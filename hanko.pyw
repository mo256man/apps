import PySimpleGUI as sg
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import win32clipboard as clp
from io import BytesIO
import os

PREVIEW_SIZE = 320                      # 20（市松模様の最小単位）で割り切れる数とする
INI_SIZE = 240                          # アウトプット（判子画像）のサイズ
INI_RATIO = 70                          # 単位はパーセント（100で割る）
COLOR4 = (217, 54, 66, 255)             # 朱色
WHITE = (255, 255, 255, 255)            # 白
BLACK = (0, 0, 0, 255)                  # 黒
TRANSPARENT = (255, 255, 255, 0)        # 透明（アルファ値なしにすると白になる）

dic_fonts = {#"行書体":"HGRGY.TTC",
         "UD教科書体": "UDDigiKyokashoN-B.ttc",
         #"ポップ体":"HGRPP1.TTC",
         "游明朝":"yumindb.ttf"}

dic_tateyoko = {0: ("横長 強", 1, 1.4),
                1: ("横長 弱", 1,1.2),
                2: ("正方形", 1,1),
                3: ("縦長 弱", 1.2,1),
                4: ("縦長 強", 1.4,1),
                }

class Frame():
    def __init__(self, image=""):
        sg.theme("Reddit")

        frame_name = sg.Frame("名前",
            [   [sg.InputText("", key="name", enable_events=True, font=("", 20), size=(18, 60))]])

        frame_toggle = sg.Frame("",
            [   [sg.Button("≡", key="設定オンオフ", font=("", 20))]], border_width=0)

        frame_dummy = sg.Frame("",
            [   [sg.Text("")]], border_width=0, size=(340,200), key="dummy")

        frame_config = sg.Frame("設定",
            [   [sg.Text("フォント　"), 
                 sg.Combo(list(dic_fonts.keys()), list(dic_fonts.keys())[0], key="font", size=(20,1), enable_events=True) ,
                ],
                [sg.Submit(button_text="□　透明", key="背景"), sg.Submit(button_text="－　横書き", key="縦横")],
                [sg.Text("印影サイズ"), 
                 sg.Slider((60,300), INI_SIZE, key="circle_slider", size=(20, None), orientation="h", enable_events=True, disable_number_display=True,),
                 sg.Text(str(INI_SIZE), key="circle_size")],
                [sg.Text("文字サイズ"), 
                 sg.Slider((50,100), INI_RATIO, key="chara_slider", size=(20, None), orientation="h", enable_events=True, disable_number_display=True,),
                 sg.Text(f"{INI_RATIO}%", key="chara_size")],
                [sg.Text("文字縦横比"), 
                 sg.Slider((0,4), 2, key="tateyoko_slider", size=(20, None), orientation="h", enable_events=True, disable_number_display=True,),
                 sg.Text(dic_tateyoko[2][0], key="tateyoko_ratio")],
                [sg.Text("先の太さ　"), 
                 sg.Slider((1,20), 5, key="thickness_slider", size=(20, None), orientation="h", enable_events=True, disable_number_display=True,),
                 sg.Text(4, key="thickness_value")],
            ],
            size=(340, 200),
            key="config",
            visible=False
        )

        frame_save = sg.Frame("保存",
            [   [sg.Submit(button_text="保存", key="保存", size=(15,2)),
                 sg.Submit(button_text="ｸﾘｯﾌﾟﾎﾞｰﾄﾞに\nコピー（白地）", key="コピー", size=(15,2)),
                ],
            ],
            size=(340, 70)
        )


        frame_preview = sg.Frame("プレビュー",
            [   [sg.Image(data=image, key="image")]])

        col1 = sg.Column([[frame_name, frame_toggle], [frame_dummy], [frame_config], [frame_save]])
        col2 = sg.Column([[frame_preview]])

        layout = [[col1, col2]]
        self.window = sg.Window("はんこメーカー", layout, resizable=False, icon="icon.ico")


class App():
    def __init__(self):
        self.circle_size = INI_SIZE
        self.chara_size = INI_RATIO
        self.name = ""
        self.font = list(dic_fonts.keys())[0]
        self.is_transparent = True                                      # 背景が透明かどうか
        self.is_vertical = True                                         # 縦書きならTrue、横書きならFalse
        self.tateyoko = 2                                               # 縦横のスライダー値
        self.thickness = 5                                              # 線の太さのスライダー値
        self.is_config_visible = False                                  # 設定フレームは見えない状態

class Hanko():
    def __init__(self, app):
        name = app.name if app.name != "" else "名前"                   # 名前　空白のときは"名前"になる
        r = app.circle_size//2                                          # 円の半径
        t = app.thickness                                               # 先の太さ

        # 名前
        font = dic_fonts[app.font]
        name_img = make_name(name, font, app.is_vertical)
        _, rw, rh = dic_tateyoko[app.tateyoko]
        w = int(2*r*app.chara_size/100/rw)
        h = int(2*r*app.chara_size/100/rh)
        name_img = name_img.resize((w, h))

        # 合成
        transparent = Image.new("RGBA", (2*r, 2*r), TRANSPARENT)        # 透明の画像
        image = transparent.copy()                                      # ベースとなるオブジェクト
        x, y = r-w//2, r-h//2                                           # 文字の左上座標
        image.paste(name_img, (x, y))                                   # ベースに文字をペースト

        # マスクの定義
        mask = transparent.copy()
        draw = ImageDraw.Draw(mask)
        draw.ellipse([0, 0, 2*r, 2*r], WHITE, WHITE, 1)                 # 塗りつぶした円
        image=Image.composite(image, transparent, mask=mask)            # 円からはみ出した部分は透明にする

        draw = ImageDraw.Draw(image)
        draw.ellipse([1, 1, 2*r-1, 2*r-1], None, COLOR4, t)             # あらためて特定の先の太さで円を描く

        # 背景が白のときの処理
        if not app.is_transparent:
            white = Image.new("RGBA", (2*r, 2*r), WHITE)                # 真っ白な画像
            white.paste(image, (0, 0), mask=image)
            image = white
        self.image = image

        # プレビュー用として、背景の市松模様と合成する
        preview_image = make_background(PREVIEW_SIZE, u=10)
        x1, y1 = image.size
        x2, y2 = preview_image.size
        x, y = (x2-x1)//2, (y2-y1)//2                               # ペーストする左上座標
        preview_image.paste(image, (x, y), mask=image)

        # プレビュー用画像はバイトとする
        imgbytes = BytesIO()
        preview_image.save(imgbytes, format="png")
        self.imgbytes = imgbytes.getvalue()


def rgba2rgb(imgPIL):
    w, h = imgPIL.size
    white = Image.new("RGBA", (w, h), WHITE)                        # 真っ白な画像
    white.paste(imgPIL, (0, 0), mask=imgPIL)
    return white.convert("RGB")


def make_name(name_origin, font, is_vartical):
    """
    名前画像を作る
    サイズは不定（調整はあとでおこなう）
    """
    fontPIL = ImageFont.truetype(font, size=200)                    # フォント　サイズは超巨大

    # 縦書きならば一文字ごとに改行を追加する
    if is_vartical:
        name = ""
        for letter in name_origin:
            name += letter + "\n"
    else:
        name = name_origin

    # ダミーのオブジェクト上で文字列を描画しサイズを取得する
    dummy_draw = ImageDraw.Draw(Image.new("L", (0,0)))
    w, h = dummy_draw.textsize(name, font=fontPIL)

    # 取得したサイズであらためて文字列を描写する
    imgPIL = Image.new("RGBA", (w, h), color=TRANSPARENT)
    draw = ImageDraw.Draw(imgPIL)
    draw.text(xy=(0,0), text=name, fill=COLOR4, font=fontPIL)
    imgPIL = imgPIL.crop(imgPIL.getbbox())

    return imgPIL

def make_background(size, u):
    """
    市松模様を作る
    size: 画像サイズ（縦横同じ正方形）
    u: 一マスの大きさ
    割り切れないとサイズが狂うので注意
    """
    color1 = (255, 255, 255, 255)
    color2 = (192, 192, 192, 255)
    unit = np.array([[color1,color2],[color2, color1]], np.uint8)           # 2*2ピクセルの市松模様
    unit = unit.repeat(u, axis=0).repeat(u, axis=1)                         # 縦と横にu倍繰り返す
    rep = size//(2*u)                                                       # 繰り返し回数
    tile = np.tile(unit, reps=(rep,rep,1))                                  # タイルを作る
    return Image.fromarray(tile)                                            # numpyをPILにする　灰色なのでRGB->BGRは不要


def save_image(name, imgPIL):
    """
    PIL画像を保存する
    """
    if name=="":
        sg.popup_ok("名前を入力してください", title="!")
    else:
        path = os.path.expanduser("~/Desktop")
        pathname = path + os.sep + f"ハンコ_{name}.png"
        imgPIL.save(pathname)


def send_to_clipboard(imgPIL):
    """
    画像をクリップボードに保存する　透過画像には非対応
    """
    output = BytesIO()
    imgPIL.save(output, "bmp")
    data = output.getvalue()[14:]
    output.close()
    clp.OpenClipboard()
    clp.EmptyClipboard()
    clp.SetClipboardData(clp.CF_DIB, data)
    clp.CloseClipboard()


def main():
    app = App()
    hanko = Hanko(app)

    # Frameはイベント取得時にはじめて表示されるので初期状態で画像を作っておく必要がある
    W = Frame(image=hanko.imgbytes).window

    while True:
        event, values = W.read()

        if event is None:                                           # ×ボタンで閉じる
            break
        elif event == "保存":
            save_image(app.name, hanko.image)
        elif event == "コピー":
            image = rgba2rgb(hanko.image)
            send_to_clipboard(image)
        elif event == "設定オンオフ":
            W["dummy"].hide_row()                                   # ダミーは隠される（上詰めされる）
            app.is_config_visible = not app.is_config_visible
            W["config"].update(visible=app.is_config_visible)
        elif event == "背景":
            app.is_transparent = not app.is_transparent
            if app.is_transparent:
                W["背景"].update("□　透明")
            else:
                W["背景"].update("■　白地")
        elif event == "縦横":
            app.is_vertical = not app.is_vertical
            if app.is_vertical:
                W["縦横"].update("｜　縦書き")
            else:
                W["縦横"].update("－　横書き")
        else:                                                       # それ以外のイベント
            app.name = values["name"]
            app.circle_size = int(values["circle_slider"])
            app.chara_size = int(values["chara_slider"])
            app.font = values["font"]
            app.tateyoko = values["tateyoko_slider"]
            app.thickness = int(values["thickness_slider"])
            W["circle_size"].update(app.circle_size)
            W["chara_size"].update(f"{app.chara_size}%")
            W["tateyoko_ratio"].update(dic_tateyoko[app.tateyoko][0])
            W["thickness_value"].update(app.thickness)

        # 以上の設定変更を織り込んであらためてハンコ画像を作る
        hanko = Hanko(app)
        W["image"].update(hanko.imgbytes)

    W.close()

if __name__=="__main__":
    main()
