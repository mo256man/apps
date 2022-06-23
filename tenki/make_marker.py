import cv2
from cv2 import aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

def arGenerator():
    for i in range(4):
        fileName = "{}.png".format(i)
        generator = aruco.drawMarker(dictionary, i, 100)
        cv2.imwrite(fileName, generator)
    cv2.waitKey(0)

arGenerator()
print("done.")