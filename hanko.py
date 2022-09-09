import PySimpleGUI as sg
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

PREVIEW_SIZE = 320
INI_SIZE = 240
INI_RATIO = 70                  # 単位はパーセント（100で割る）
COLOR = (66, 54, 217)           # 朱色
COLOR4 = (66, 54, 217, 255)     # 朱色
FONTS = {"行書体":"HGRGY.TTC",
         "UD教科書体": "UDDigiKyokashoN-B.ttc",
         "ポップ体":"HGRPP1.TTC",
         }

class Frame():
    def __init__(self, hanko):
        h, w = hanko.image.shape[:2]
        sg.theme("Reddit")

        frame_name = sg.Frame("名前",
            [
                [sg.InputText("", key="name", enable_events=True,)]
            ],
            size=(340, 50)
        )

        frame_config = sg.Frame("設定",
            [
                [sg.Text("印影サイズ"), 
                 sg.Slider((32,320), INI_SIZE, key="circle_size", orientation="h", enable_events=True, disable_number_display=True,),
                 sg.Text(str(INI_SIZE), key="circle_value")],
                [sg.Text("文字サイズ"), 
                 sg.Slider((50,100), INI_RATIO, key="chara_size", orientation="h", enable_events=True, disable_number_display=True,),
                 sg.Text(str(INI_RATIO), key="chara_value")],
                [sg.Text("フォント　"), 
                 sg.Combo(list(FONTS.keys()), list(FONTS.keys())[0], key="font", size=(100,None)) ,
                ],
                [sg.Submit(button_text="作成", key="start")],
            ],
            size=(340, 300)
        )
        frame_preview = sg.Frame("プレビュー",
            [
                [sg.Image(data=hanko.imgbytes, key="image")]
            ],
            size=(PREVIEW_SIZE, PREVIEW_SIZE)
        )

        col1 = sg.Column([[frame_name],[frame_config]])
        col2 = sg.Column([[frame_preview]])

#        layout = [[frame1, frame2], frame_preview]
        layout = [[col1, col2]]
        self.window = sg.Window("はんこメーカー", layout, resizable=False)


class Hanko():
    def __init__(self, name, size, ratio, font):
        r = size//2                                                 # 円の半径
        back_image = make_background(PREVIEW_SIZE)
        if name == "":
            name = "名前"

        image = np.full((size,size,4), (255,255,255, 0), np.uint8)
        mask_cirlce = image.copy()

        # 縦書きの名前
        name_image = make_name(name, font)
        w = int(size*ratio/100)
        h = w
        name_image = cv2.resize(name_image, (w, h))
        x, y = r-w//2, r-h//2                                       # 文字の左上座標
        image[y:y+h, x:x+w] = name_image

        # 塗りつぶした丸のマスクを作り、それからはみ出した部分を透過色にする
        cv2.circle(mask_cirlce, (r,r), r, COLOR4, -1)
        image = np.where(mask_cirlce==(0,0,0,0), mask_cirlce, image)

        # あらためて特定の線の太さで丸を描く
        cv2.circle(image, (r,r), r-2, COLOR4, 5)

        self.image = image

        # プレビュー用として、バックグラウンドと合成する
        if size < PREVIEW_SIZE:
            preview_image = np.full((PREVIEW_SIZE,PREVIEW_SIZE,4), (0,0,0,0), np.uint8)
            x = PREVIEW_SIZE//2 - r
            y = x
            preview_image[y:y+size, x:x+size] = image
        else:
            x = r - PREVIEW_SIZE//2
            y = x
            preview_image = image[y:y+PREVIEW_SIZE, x:x+PREVIEW_SIZE]

        img3 = preview_image[:, :, :3]
        mask1 = preview_image[:, :, 3]
        mask3 = cv2.merge((mask1, mask1, mask1))
        preview_image = np.where(mask3==(0,0,0), back_image, img3)


        # self.preview = back_image
        self.imgbytes = cv2.imencode('.png', preview_image)[1].tobytes()


def make_name(name, font):
    fontPIL = ImageFont.truetype(font, size=200)

    tate_name = ""
    for letter in name:
        tate_name += letter + "\n"
    tate_name = tate_name[:-1]

    # 実際に描画する前にダミーのオブジェクト上で描画し
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (0,0)))
    w, h = dummy_draw.textsize(tate_name, font=fontPIL)
    h += 200//10
    
    imgPIL = Image.new("RGBA", (w, h), color=(255,255,255,0))
    draw = ImageDraw.Draw(imgPIL)
    draw.text(xy=(0,0), text=tate_name, fill=COLOR, font=fontPIL)
    return np.array(imgPIL)


def make_background(size, u=20):
    imgH, imgW = size, size
    color1 = (255, 255, 255)
    color2 = (192, 192, 192)
    imat = np.array([[color1,color2],[color2, color1]], np.uint8)
    unit = cv2.resize(imat, (2*u,2*u), interpolation=cv2.INTER_NEAREST)
    rh, rw = int(imgH/2/u), int(imgW/2/u)
    tile = np.tile(unit, reps=(rh,rw,1))
    return tile


def main():
    hanko = Hanko("", INI_SIZE, INI_RATIO, list(FONTS.values())[0])
    f = Frame(hanko)
    while True:
        # ウィンドウ表示
        event, values = f.window.read()

        if event is None:                   # ×ボタンで閉じる
            break
        else:                               # それ以外のイベント
            name = values["name"]
            size = int(values["circle_size"])
            font = FONTS[values["font"]]
            print(font)
            
            f.window["circle_value"].update(str(size))

            ratio = int(values["chara_size"])
            f.window["chara_value"].update(f"{ratio}%")

            hanko = Hanko(name, size, ratio, font)
            imgbytes = hanko.imgbytes
            f.window["image"].update(data=imgbytes)

    f.window.close()

if __name__=="__main__":
    main()