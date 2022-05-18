import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from app_base64 import img2base64

def cv2_putText(img, text, org, fontFace, fontScale, color, mode=0):
    """
    OpenCV画像に日本語テキストを描写する　BGRA前提
    mode:文字の位置の起点　0=左下　1=左上　2=中央
    """

    # テキスト描写域を取得
    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("L", (0,0)))                  # ここは描画サイズを取得するためなのでL（グレー）でも可
    text_w, text_h = dummy_draw.textsize(text, font=fontPIL)
    text_b = int(0.1 * text_h)

    # テキスト描写域の左上座標を取得（元画像の左上を原点とする）
    x, y = org
    offset_x = [0, 0, text_w//2]
    offset_y = [text_h, 0, (text_h+text_b)//2]
    x0 = x - offset_x[mode]
    y0 = y - offset_y[mode]
    img_h, img_w = img.shape[:2]

    # 画面外なら何もしない
    if not ((-text_w < x0 < img_w) and (-text_b-text_h < y0 < img_h)) :
        print ("out of bounds")
        return img

    # テキスト描写域の中で元画像がある領域の左上と右下（元画像の左上を原点とする）
    x1, y1 = max(x0, 0), max(y0, 0)
    x2, y2 = min(x0+text_w, img_w), min(y0+text_h+text_b, img_h)

    # テキスト描写域と同サイズの黒画像を作り、それの全部もしくは一部に元画像を貼る
    text_area = np.zeros((text_h+text_b,text_w, 4), dtype=np.uint8)
    text_area[y1-y0:y2-y0, x1-x0:x2-x0] = img[y1:y2, x1:x2]

    # それをPIL化し、フォントを指定してテキストを描写する（色変換なし）
    imgPIL = Image.fromarray(text_area)
    draw = ImageDraw.Draw(imgPIL)
    draw.text(xy = (0, 0), text = text, fill = color, font = fontPIL)

    # PIL画像をOpenCV画像に戻す（色変換なし）
    text_area = np.array(imgPIL, dtype = np.uint8)

    # 元画像の該当エリアを、文字が描写されたものに更新する
    img[y1:y2, x1:x2] = text_area[y1-y0:y2-y0, x1-x0:x2-x0]

    return img

def get_attribue(dict, key, default_value):
    value = dict.get(key)                                       # request.formから取り出した値はすべて文字列になる
    if value is None:                                           # 辞書にそのようなキーがなければ
        value = default_value                                   # 事前に設定したデフォルト値とする
    elif key in ["width", "height", "radius", "thickness", "fontsize"]:      # キーがあったとき、それがリスト内の項目ならば
        value = int(value)                                      # 値を文字列から整数にする
    return value



class Hanko():
    def __init__(self, dict):
        self.text = get_attribue(dict, "text", "")
        self.width = get_attribue(dict, "width", 200)
        self.height = get_attribue(dict, "height", 200)
        self.radius = get_attribue(dict, "radius", 20)
        self.thickness = get_attribue(dict, "thickness", 10)
        self.font = get_attribue(dict, "font", "UDDigiKyokashoN-B.ttc")
        self.fontsize = get_attribue(dict, "fontsize", 50)
        self.forecolor = get_attribue(dict, "forecolor", (0,0,255))
        self.bgcolor = get_attribue(dict, "bgcolor", None)

        if self.radius < self.thickness:
            self.radius = self.thickness

        image = self.make_round_rectangle()

        if self.text != "":
            self.text = self.text.replace("\r\n", "\n")     # textareaの改行コードは \n なのだが、いつの間にか \r\n になっている
            image = cv2_putText(image, self.text, (self.width//2, self.height//2), self.font, self.fontsize, self.forecolor, 2)
        
        # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)        # gray -> BGRAにする
        # img4 = imgB = cv2.merge((255-image,255-image,255-image,image))

        # dst = np.where(image[..., np.newaxis] == 0, (255,0,0), (0,255,255)).astype(np.uint8)

        self.strB64 = "data:image/png;base64," + img2base64(image)

    def make_round_rectangle(self):
        """
        角丸四角形を作る
        """
        w, h = self.width, self.height
        image = np.zeros((h, w, 4), np.uint8)          # ベース画像は(0,0,0,0)すなわち全透過
        forecolor = list(self.forecolor)                         # タプルをリストにする
        forecolor.append(255)                                 # アルファ値255を追加
        if self.bgcolor is None:                                     # bgcolorがNoneならば
            bgcolor = (0,0,0,0)                                 # 全透過にする
        else:                                                   # さもなくば
            bgcolor = list(self.bgcolor)                             # タプルをリストにする
            bgcolor.append(255)                                 # アルファ値255を追加

        t = int(self.thickness/2)
        r = self.radius-t

        # ベースの内側塗りつぶし
        cv2.rectangle(image, (r, t), (w-1-r, h-1-t), bgcolor, -1)                              # 背景色で矩形（塗りつぶす）
        cv2.rectangle(image, (t, r), (w-1-t, h-1-r), bgcolor, -1)

        # コーナー部分
        cx, cy = w//2, h//2                                                             # 画像の中央
        dirs = [(1,1), (-1,1), (-1,-1), (1,-1)]                                         # x方向y方向のベクトル
        for i, (dx, dy) in enumerate(dirs):
            x, y = cx + dx*cx - dx*self.radius, cy + dy * cy - dy * self.radius         # 中心座標
            cv2.ellipse(image, (x,y), (r,r), 0, i*90, (i+1)*90, bgcolor, -1)            # 前景色で扇形（塗りつぶす）   
            cv2.ellipse(image, (x,y), (r,r), 0, i*90, (i+1)*90, forecolor, 
                        self.thickness, cv2.LINE_AA)                                    # 前景色で弧（塗りつぶさない）

        # ストレート部分
        r = self.radius
        pts = [[(r, t), (w-1-r, t)],
            [(r, h-1-t), (w-1-r, h-1-t)],
            [(t, r), (t, h-1-r)],
            [(w-1-t, r), (w-1-t, h-1-r)]]                                               # 始点終点のリスト
        for pt in pts:
            cv2.line(image, pt[0], pt[1], forecolor, self.thickness)                                       # 前景色で線

        return image

if __name__ == "__main__":
    pass