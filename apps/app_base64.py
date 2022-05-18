import base64
import cv2

def img2base64(imgCV):
    _, imgEnc = cv2.imencode(".png", imgCV)     # エンコードされたオブジェクト
    imgB64 = base64.b64encode(imgEnc)           # byte
    strB64 = str(imgB64, "utf-8")               # string
    return strB64
