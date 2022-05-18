from enum import EnumMeta
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def make_round_rectangle(radius, base=None, size=None, color=(255,255,255)):
    """
    塗りつぶされた角丸四角形を作る
    ベースがない場合はサイズの指定が必須
    ベースがある場合はサイズの指定が任意
        サイズがない場合、ベース画像のサイズの角丸四角形を作る
        サイズがある場合、画像中央に指定したサイズで角丸四角形を作る
    """
    if base is None:
        width, height = size
        image = np.zeros((height, width, 4), np.uint8)
        imgH, imgW = image.shape[:2]
        height, width = imgH, imgW
    else:
        image = base.copy()
        imgH, imgW = image.shape[:2]
        if size is None:
            width, height = imgW, imgH
        else:
            width, height = size

    color = list(color)         # タプルをリストにする
    color.append(255)           # アルファ値255を追加


    cx, cy = width//2, height//2
    roi = image[imgH//2-cy:imgH//2+cy, imgW//2-cx:imgW//2+cx]

    # 角丸以外のストレート部分を描写　OpenCVを使わずnumpyで
    roi[radius:height-radius, :] = color
    roi[:, radius:width-radius] = color

    # 角丸部分 扇型ではなく普通に円を描く
    dirs = [(1,1), (-1,1), (-1,-1), (1,-1)]
    for i, d in enumerate(dirs):
        dx, dy = d
        x1, y1 = cx+dx*cx, cy+dy*cy
        x2, y2 = x1-dx*radius, y1-dy*radius
        cv2.circle(roi, (x2,y2), radius, color, -1, cv2.LINE_AA)
    
    image[imgH//2-cy:imgH//2+cy, imgW//2-cx:imgW//2+cx] = roi
    return image



def make_round_frame(size, radius, thickness, color):
    width, height = size
    image = np.full((height, width, 4),(0,0,0,0) , np.uint8)      # ベース画像は全透過とする
    image = make_round_rectangle(radius, None, size, color)

    width, height = size
    new_size = (width-2*thickness, height-2*thickness)
    image = make_round_rectangle(radius-thickness, image, new_size, (255,255,255))
    return image
    

image = make_round_frame((250,250), 100, 20, (0,255,255))
#image = make_round_rectangle(50, None, (400,300))
cv2.imshow("image", image)
print(image[0][0])
print(image[100][100])
cv2.imwrite("image.png", image)
cv2.waitKey()
cv2.destroyAllWindows()
