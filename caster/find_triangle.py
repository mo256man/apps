import cv2
import numpy as np

img = cv2.imread("shapes_image.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY) # 画像を二値化
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 領域検出

triangles = 0  # 三角形カウント用
#抽出した領域を1つずつ取り出し輪郭を近似する。三角形の場合、輪郭を赤くする
for cnt in contours:
    epsilon = 0.1*cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    if len(approx) == 3: 
        cv2.drawContours(img, [approx], 0, (0, 0, 255), 2)
        triangles += 1

print(triangles)  # 三角形の数を表示
cv2.imshow("", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
