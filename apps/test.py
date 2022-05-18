from enum import EnumMeta
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def make_round_rectangle(size, radius, bordercolor, bgcolor, thickness):
    """
    角丸四角形を作る
    """
    width, height = size
    image = np.zeros((height, width, 4), np.uint8)          # ベース画像は(0,0,0,0)すなわち全透過
    bordercolor = list(bordercolor)                         # タプルをリストにする
    bordercolor.append(255)                                 # アルファ値255を追加
    if bgcolor is None:                                     # bgcolorがNoneならば
        bgcolor = (0,0,0,0)                                 # 全透過にする
    else:                                                   # さもなくば
        bgcolor = list(bgcolor)                             # タプルをリストにする
        bgcolor.append(255)                                 # アルファ値255を追加

    t = int(thickness/2)
    r = radius-t

    # ベースの内側塗りつぶし
    cv2.rectangle(image, (r, t), (width-1-r, height-1-t), bgcolor, -1)                              # 背景色で矩形（塗りつぶす）
    cv2.rectangle(image, (t, r), (width-1-t, height-1-r), bgcolor, -1)

    # コーナー部分
    cx, cy = width//2, height//2                                                                    # 画像の中央
    dirs = [(1,1), (-1,1), (-1,-1), (1,-1)]                                                         # x方向y方向のベクトル
    for i, (dx, dy) in enumerate(dirs):
        x, y = cx + dx*cx - dx*radius, cy + dy * cy - dy * radius                                   # 中心座標
        cv2.ellipse(image, (x,y), (r,r), 0, i*90, (i+1)*90, bgcolor, -1)                            # 背景色で扇形（塗りつぶす）
        cv2.ellipse(image, (x,y), (r,r), 0, i*90, (i+1)*90, bordercolor, thickness, cv2.LINE_AA)    # 前景色で弧（塗りつぶさない）
        cv2.imshow("image", image)
        cv2.waitKey()
    # ストレート部分
    r = radius
    pts = [[(r, t), (width-1-r, t)],
           [(r, height-1-t), (width-1-r, height-1-t)],
           [(t, r), (t, height-1-r)],
           [(width-1-t, r), (width-1-t, height-1-r)]]                                               # 始点終点のリスト
    for pt in pts:
        cv2.line(image, pt[0], pt[1], bordercolor, thickness)                                       # 前景色で線

    return image



image = make_round_rectangle((200,200), 100, (0,0,255), (255,255,255), 20)
cv2.imshow("image", image)
cv2.imwrite("image.png", image)
cv2.waitKey()
cv2.destroyAllWindows()
