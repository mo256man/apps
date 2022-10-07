import cv2

img1 = cv2.imread("c1.png")
img2 = cv2.imread("c2.png")
imdiff = cv2.absdiff(img1, img2)

cv2.imshow("diff", imdiff)
cv2.waitKey(0)
cv2.imwrite("diff.png", imdiff)
cv2.destroyAllWindows()
