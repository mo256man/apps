import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import sys

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)

def cv2_putText(img, text, org, fontFace="BIZ-UDGothicR.ttc", fontScale=20, color=BLACK, mode=1):
# cv2.putText()にないオリジナル引数「mode」　orgで指定した座標の基準
# 0（デフォ）＝cv2.putText()と同じく左下　1＝左上　2＝中央

    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0,0)))
    text_w, text_h = dummy_draw.textsize(text, font=fontPIL)
    text_b = int(0.1 * text_h)

    x, y = org
    offset_x = [0, 0, text_w//2]
    offset_y = [text_h, 0, (text_h+text_b)//2]
    x0 = x - offset_x[mode]
    y0 = y - offset_y[mode]
    img_h, img_w = img.shape[:2]

    # 画面外なら何もしない
    if not ((-text_w < x0 < img_w) and (-text_b-text_h < y0 < img_h)) :
        return img

    x1, y1 = max(x0, 0), max(y0, 0)
    x2, y2 = min(x0+text_w, img_w), min(y0+text_h+text_b, img_h)
    text_area = np.full((text_h+text_b,text_w,3), (0,0,0), dtype=np.uint8)
    text_area[y1-y0:y2-y0, x1-x0:x2-x0] = img[y1:y2, x1:x2]
    imgPIL = Image.fromarray(text_area)
    draw = ImageDraw.Draw(imgPIL)
    draw.text(xy = (0, 0), text = text, fill = color, font = fontPIL)
    text_area = np.array(imgPIL, dtype = np.uint8)
    img[y1:y2, x1:x2] = text_area[y1-y0:y2-y0, x1-x0:x2-x0]
    return img

class Box():
    def __init__(self, name, num, size, height):
        self.name = name
        self.num = num
        self.size1 = max(size)
        self.size2 = min(size)
        self.height = height

class Canvas():
    def __init__(self):
        self.title = "nidumi sim"
        self.image = np.full((768, 1024, 3), (255,255,255), np.uint8)
        self.image = cv2_putText(self.image, "荷積みシミュレータ", (20,20), fontScale=40)
        self.x0 = 200   # スキット描写の原点
        self.y0 = 250
        self.step = 50
        self.draw_skit()

    def draw_skit(self):
        for x in range(self.x0, self.x0+10*self.step+1, self.step):
            for y in range(self.y0, self.y0+10*self.step+1, self.step):
                cv2.line(self.image, (x, self.y0), (x, self.y0+10*self.step), (50,50,50), 1)
                cv2.line(self.image, (self.x0, y), (self.x0+10*self.step, y), (50,50,50), 1)

    def draw_baggages(self, baggages):
        for i, baggage in enumerate(baggages):
            cv2_putText(self.image, f"{baggage.name}  が {baggage.num}箱　サイズ=({baggage.size1}x{baggage.size2}x高さ{baggage.height}）", (100,80+20*i), fontScale=20)

    def draw_box(self, floor, baggage, i, x, y, tateyoko):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)        # グレースケール画像にする
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)        # グレーのBGR画像にする
        x0, y0 = 200, 200
        if tateyoko==0:                                     # 1回目の縦横定義
            length, width = baggage.size1, baggage.size2
            tateyoko_msg = "縦長に"
        else:                                               # 2回目は縦横を反転する
            length, width = baggage.size2, baggage.size1
            tateyoko_msg = "横長に"
        cv2.rectangle(self.image, (x0,y0), (1024,y0+40), WHITE, -1)
        cv2_putText(self.image, f"{i+1}個目の{baggage.name}を{floor}階の({x},{y})に{tateyoko_msg}設置", (x0,y0), fontScale=24)
        x1 = self.x0 + x*self.step
        y1 = self.y0 + y*self.step
        x2 = x1 + width*self.step
        y2 = y1 + length*self.step
        color = (int(255*(1-floor/10)), 0, 0)
        cv2.rectangle(self.image, (x1,y1), (x2,y2), color, -1)
        cv2.rectangle(self.image, (x1,y1), (x2,y2), RED, 2)
        self.image = cv2_putText(self.image, f"{baggage.name}\n{i+1}個目\n高さ{floor+baggage.height}階", ((x1+x2)//2,(y1+y2)//2), color=RED, mode=2)

    def draw(self):
        cv2.imshow(self.title, self.image)
        key = cv2.waitKey(0)
        if key & 0xFF == 27:        # esc
            sys.exit()

    def end(self):
        x0, y0 = 200, 200
        cv2.rectangle(self.image, (x0,y0), (1024,y0+40), WHITE, -1)
        self.image = cv2_putText(self.image, "完了", (x0, y0), color=BLACK)


baggages = [
    Box("TP632", 5, (6,3), 2),
    Box("TP433", 4, (5,3), 3),
    Box("TP331", 4, (3,3), 1),
]

skit = np.zeros((10,10), np.uint8)
canvas = Canvas()
canvas.draw_baggages(baggages)
canvas.draw()
for baggage in baggages:
    for i in range(baggage.num):
        print(f"{i+1}個目の{baggage.name}について")
        min_floor = np.min(skit)
        max_floor = np.max(skit)
        for floor in range(min_floor, max_floor+1):
            is_found = False
            for tateyoko in range(2):                               # 2周する
                if tateyoko==0:                                     # 1回目の縦横定義
                    length, width = baggage.size1, baggage.size2
                    tateyoko_msg = "縦長に"
                else:                                               # 2回目は縦横を反転する
                    length, width = baggage.size2, baggage.size1
                    tateyoko_msg = "横長に"

                for y in range(10-length):
                    for x in range(10-width):
                        roi = skit[y:y+length, x:x+width]
                        if np.all(roi==floor):      # 注目エリアすべてが注目階だったら
                            is_found = True
                            print(f"{floor}階の({x},{y})に{tateyoko_msg}配置")
                            skit[y:y+length, x:x+width] += baggage.height
                            # print(skit)
                            canvas.draw_box(floor, baggage, i, x, y, tateyoko)
                            canvas.draw()
                            break
                        else:
                            print(f"{floor}階の({x},{y})には置けなかった")
                            pass
                    if is_found:
                        break
                if is_found:
                    break
            if is_found:
                break
canvas.end()
canvas.draw()
