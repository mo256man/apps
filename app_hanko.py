import cv2
from matplotlib.pyplot import text
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from app_base64 import img2base64
from app_cv import *

def get_attribue(dict, key, default_value):
    if key == "enhance":                                                            # enhanceは複数ボタンを持つラジオボタンなので特別な処理をする
        try:
            value = int(dict.getlist(key)[0])                                       # dict.getlist(key)でボタンが押されているリストを得る
        except:
            value = 0
    else:
        value = dict.get(key, default_value)                                        # キーから値を取得する キーがなければデフォ値とする
        numeric_keys = ["width", "height", "radius", "thickness", "fontsize"]       # 値が数値となるキーのリスト（request.formから取り出した値はすべて文字列になる）
        if key in numeric_keys:                                                     # キーが数値キーならば
            value = int(value)                                                      # 値を文字列から整数にする
    return value


class Hanko():
    def __init__(self, dict):
        self.text = get_attribue(dict, "text", "サン\nプル")
        self.width = get_attribue(dict, "width", 200)
        self.height = get_attribue(dict, "height", 200)
        self.radius = get_attribue(dict, "radius", 20)
        self.thickness = get_attribue(dict, "thickness", 10)
        self.font = get_attribue(dict, "font", "UDDigiKyokashoN-B.ttc")
        self.fontsize = get_attribue(dict, "fontsize", 50)
        self.forecolor = get_attribue(dict, "forecolor", (0,0,255))
        self.enhance = get_attribue(dict, "enhance", 0)

        if self.radius < self.thickness:
            self.radius = self.thickness

        """
        枠描画はPILだとアンチエイリアス処理ができず美しくないためOpenCVが適している
        日本語テキスト描画はPILを使う
        透過処理はどちらでも可
        以上より、ベース画像はOpenCVとし、日本語テキスト描画の部分はPILに変換しておこなう　ただし従来の我が関数は使わない
        """

        # マスク（グレースケールのはんこ）を作る
        mask = self.make_round_rectangle_CV()

        # 文字列を描写する　ここをクラス関数にする
        maskPIL = Image.fromarray(mask)                                     # OpenCV画像をPIL画像にする
        fontPIL = ImageFont.truetype(font = self.font, size = self.fontsize)
        if self.text != "":
            self.text = self.text.replace("\r\n", "\n")                     # textareaの改行コードは \n なのだが、いつの間にか \r\n になっている
            draw = ImageDraw.Draw(Image.new("L", (0,0)))                    # 文字描画サイズを取得するためのダミーdrawオブジェクト（サイズ0）
            _, _, w, h = draw.textbbox((0,0), self.text, font=fontPIL)      # 文字描写エリアのバウンディングボックスを取得
            textPIL = Image.new("L",(w, h))                                 # サイズを指定してあらためてImageオブジェクトを作る
            draw = ImageDraw.Draw(textPIL)                                  # Imageのdrawオブジェクト
            draw.text((0,0), self.text, font=fontPIL, fill=255)             # 文字描写

            if self.enhance==1:
                textPIL = textPIL.resize((self.width-2*self.radius, self.height-2*self.radius))
                x, y = self.radius, self.radius
            else:
                x, y = (self.width-w)//2, (self.height-h)//2
            maskPIL.paste(textPIL, (x,y))                

        mask = np.array(maskPIL)                                            # PILをOpenCVに戻す

        #if self.text != "":
        #    self.text = self.text.replace("\r\n", "\n")     # textareaの改行コードは \n なのだが、いつの間にか \r\n になっている
        #    mask = cv2_putText(mask, self.text, (self.width//2, self.height//2), self.font, self.fontsize, 255, 2)
            
            #pos = (self.radius, self.radius)                                # 最大モードにおける左上座標
            #size = (self.width-2*self.radius, self.height-2*self.radius)    # 最大モードにおける文字列描画域サイズ
            #mode = 1                                                        # 最大モードにおける文字列描画基準位置（左上）
            #mask = draw_letters(mask, self.text, (self.width//2, self.height//2), self.font, self.fontsize, 255, mode)


        # マスクに色を付ける＋アルファ値を調整する
        # image = np.full((self.height, self.width,3), self.forecolor, np.uint8)
        image = get_gradient_3d(self.width, self.height, (0, 0, 192), (255, 255, 64), (True, False, False))
        image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2BGRA)

        # マスクのない部分を透過色にする
        image[:,:,0] = np.where(mask==0, 0, image[:,:,0])
        image[:,:,1] = np.where(mask==0, 0, image[:,:,1])
        image[:,:,2] = np.where(mask==0, 0, image[:,:,2])
        image[:,:,3] = mask

        self.image = image
        cv2.imwrite("image.png", image)
        self.strB64 = "data:image/png;base64," + img2base64(image)


    def make_round_rectangle_pil(self):
        """
        角丸四角形を作る　グレー前提
        """
        w, h = self.width, self.height
        image = Image.new("L", (w, h))
        draw = ImageDraw.Draw(image)
        t = int(self.thickness/2)
        r = self.radius-t

        # コーナー部分
        cx, cy = w//2, h//2                                                             # 画像の中央
        dirs = [(1,1), (-1,1), (-1,-1), (1,-1)]                                         # x方向y方向のベクトル
        for i, (dx, dy) in enumerate(dirs):
            x0, y0 = (1+dx)*cx, (1+dy)*cy                                               # コーナー座標
            x1, y1 = x0 - 2*dx*self.radius, y0 - 2*dy*self.radius                       # コーナーの内側の座標
            x0, x1 = min(x0, x1), max(x0,x1)                                            # 左上を(x0,y0)、右下を(x1,y1)とする
            y0, y1 = min(y0, y1), max(y0,y1)                                            # （PILの仕様）

            draw.arc(((x0,y0),(x1,y1)), i*90, (i+1)*90, 255, self.thickness)            # 円弧

        # ストレート部分
        r = self.radius
        pts = [[(r, t), (w-1-r, t)],
               [(r, h-1-t), (w-1-r, h-1-t)],
               [(t, r), (t, h-1-r)],
               [(w-1-t, r), (w-1-t, h-1-r)]]                                            # 始点終点のリスト
        for pt in pts:
            draw.line((pt[0], pt[1]), 255, self.thickness)                              # 線

        return np.asarray(image)

    def make_round_rectangle_CV(self):
        """
        角丸四角形を作る　グレー前提
        """
        w, h = self.width, self.height
        image = np.zeros((h, w), np.uint8)                                              # マスク（黒字に白で描写する）

        t = int(self.thickness/2)
        r = self.radius-t

        # コーナー部分
        cx, cy = w//2, h//2                                                             # 画像の中央
        dirs = [(1,1), (-1,1), (-1,-1), (1,-1)]                                         # x方向y方向のベクトル
        for i, (dx, dy) in enumerate(dirs):
            x, y = cx + dx*cx - dx*self.radius, cy + dy * cy - dy * self.radius         # 中心座標
            cv2.ellipse(image, (x,y), (r,r), 0, i*90, (i+1)*90, 255,
                        self.thickness, cv2.LINE_AA)                                    # 円弧

        # ストレート部分
        r = self.radius
        pts = [[(r, t), (w-1-r, t)],
               [(r, h-1-t), (w-1-r, h-1-t)],
               [(t, r), (t, h-1-r)],
               [(w-1-t, r), (w-1-t, h-1-r)]]                                            # 始点終点のリスト
        for pt in pts:
            cv2.line(image, pt[0], pt[1], 255, self.thickness)                          # 線

        return image



if __name__ == "__main__":
    hanko = Hanko({})
    cv2.imshow("hanko", cv2.resize(hanko.image, None, fx=5,fy=5))
    cv2.imwrite("image.png", hanko.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
