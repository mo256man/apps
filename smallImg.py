import cv2

filename = "mario.jpg"

img = cv2.imread(filename)
img = cv2.resize(img, (16,16), interpolation = cv2.INTER_NEAREST)
cv2.imshow("img", img)
cv2.waitKey()
cv2.destroyAllWindows()
cv2.imwrite("mario.png", img)