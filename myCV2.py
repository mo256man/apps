import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def cv2_putText(img, text, org, fontFace, fontScale, color, mode=None, anchor=None):
    """
    mode:
        0:left bottom, 1:left ascender, 2:middle middle,
        3:left top, 4:left baseline
    anchor:
        lb:left bottom, la:left ascender, mm: middle middle,
        lt:left top, ls:left baseline
    """

    # テキスト描写域を取得
    x, y = org
    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("L", (0,0)))
    xL, yT, xR, yB = dummy_draw.multiline_textbbox((x, y), text, font=fontPIL)

    # modeおよびanchorによる座標の変換
    img_h, img_w = img.shape[:2]
    if mode is None and anchor is None:
        offset_x, offset_y = xL - x, yB - y
    elif mode == 0 or anchor == "lb":
        offset_x, offset_y = xL - x, yB - y
    elif mode == 1 or anchor == "la":
        offset_x, offset_y = 0, 0
    elif mode == 2 or anchor == "mm":
        offset_x, offset_y = (xR + xL)//2 - x, (yB + yT)//2 - y
    elif mode == 3 or anchor == "lt":
        offset_x, offset_y = xL - x, yT - y
    elif mode == 4 or anchor == "ls":
        _, descent = ImageFont.FreeTypeFont(fontFace, fontScale).getmetrics()
        offset_x, offset_y = xL - x, yB - y - descent

    x0, y0 = x - offset_x, y - offset_y
    xL, yT = xL - offset_x, yT - offset_y
    xR, yB = xR - offset_x, yB - offset_y

    # バウンディングボックスを描画　不要ならコメントアウトする
    #cv2.rectangle(img, (xL,yT), (xR,yB), color, 1)

    # 画面外なら何もしない
    if xR<=0 or xL>=img_w or yB<=0 or yT>=img_h:
        print("out of bounds")
        return img

    # ROIを取得する
    x1, y1 = max([xL, 0]), max([yT, 0])
    x2, y2 = min([xR, img_w]), min([yB, img_h])
    roi = img[y1:y2, x1:x2]

    # ROIをPIL化してテキスト描画しCV2に戻る
    roiPIL = Image.fromarray(roi)
    draw = ImageDraw.Draw(roiPIL)
    draw.text((x0-x1, y0-y1), text, color, fontPIL)
    roi = np.array(roiPIL, dtype=np.uint8)
    img[y1:y2, x1:x2] = roi

    return img

if __name__ == "__main__":
    pass
