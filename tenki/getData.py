from datetime import datetime
import numpy as np
import cv2
import base64

def img2b64(image):
    _, img_enc = cv2.imencode(".jpg", image)                    # jpg形式でエンコード
    img_bin = img_enc.tobytes()                                 # それをバイトにする 
    imgb64 =  base64.b64encode(img_bin)                         # それをbase64にする
    return imgb64.decode("utf-8")                               # それを文字列にして返す


class Results():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.status = ""
        self.mos_size_init = 20
        self.mos_size = self.mos_size_init

    def refresh(self, data_from_ajax):

        # ajaxから送られてきたデータを元に処理をする
        btn = data_from_ajax.get("button")
        if btn is not None:
            if btn == 0:
                self.mos_size = self.mos_size_init
            else:
                self.mos_size = self.mos_size + btn if self.mos_size > 1 else self.mos_size

        self.date = datetime.now().strftime("%H:%M:%S")
        _, frame = self.cap.read()                              # 普通のOpenCV画像（Numpy配列）

        # 画像その1　カメラそのまま
        image1 = frame.copy()
        img1 = img2b64(image1)

        # 画像その2　画像処理を加える
        image2 = frame.copy()
        h, w = image2.shape[:2]
        image2 = cv2.resize(image2, dsize=(w//self.mos_size, h//self.mos_size))
        image2 = cv2.resize(image2, dsize=(w, h), interpolation=cv2.INTER_NEAREST)
        img2 = img2b64(image2)

        self.json = {"date": self.date,
                     "img1": img1,
                     "img2": img2,
                     "status": self.status
                     }
