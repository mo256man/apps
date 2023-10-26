import numpy as np
import cv2

base = np.full((80, 80, 4), (0,0,0,0), np.uint8)
BLACK = (64,64,64,255)
GRAY =  (240,240,240,255)
WHITE = (255,255,255,255)
RED = (0,0,255,255)
BLUE = (255,0,0,255)
GREEN = (0,255,0,255)
ORANGE = (32,130,245,255)
LINE = (12,12,12,255)

colors = [RED, BLUE, GREEN, ORANGE, BLACK]
names = ["Red", "Blue", "Green", "Orange", "Black"]

for color, name in zip(colors, names):
    image = base.copy()
    cv2.circle(image, (40,40), 38, GRAY, -1)
    cv2.circle(image, (40,40), 38, LINE, 2)
    cv2.circle(image, (40,40), 34, color, -1)
    cv2.circle(image, (40,40), 34, LINE, 1)

    cv2.imwrite(f"btn{name}On.png", image)

    img_bgr = np.full((1,1,3), color[:3], np.uint8)
    img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    img_hsv[:,:,(0)] = img_hsv[:,:,(0)]+0 # 色相の計算
    img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*1 # 彩度の計算
    img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*0.3 # 明度の計算
    img_bgr = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
    new_color = img_bgr[0,0]
    new_color = np.asarray(new_color)
    b, g, r = new_color
    new_color = (int(b), int(g), int(r), 255)
    image = base.copy()
    cv2.circle(image, (40,40), 38, GRAY, -1)
    cv2.circle(image, (40,40), 38, LINE, 2)
    cv2.circle(image, (40,40), 34, new_color, -1)
    cv2.circle(image, (40,40), 34, LINE, 1)
    cv2.imwrite(f"btn{name}Off.png", image)

print("done.")