import numpy as np
import cv2
import random

class Viewer():
    def __init__(self, dic):
        self.images = []
        self.titles = []
        for title, filename in dic.items():
            image = cv2.imread(filename)
            self.images.append(image)
            self.titles.append(title)

        self.winname = "synchro viewer"                     # ウィンドウ名
        self.cnt = len(dic)                                 # 画像の数
        self.imgH, self.imgW = self.images[0].shape[:2]     # 各画像のサイズ（全部同じの前提）
        self.WINH, self.WINW = 300, 300                     # 画像表示窓のサイズ（定数）
        self.roiH, self.roiW = self.WINH, self.WINW         # ROIのサイズの初期値
        self.screen = np.zeros((self.WINH, self.cnt*self.WINW, 3), np.uint8)    # アプリ全体
        self.x0, self.y0 = (self.imgW-self.WINW)//2, (self.imgH-self.WINH)//2   # 画像表示左上初期値
        self.ix, self.iy = 0, 0
        self.BAI = 1.2                                      # 倍率の底（定数）
        self.k = 0                                          # 倍率の対数

        self.fontFace, self.fontScale, self.thickness = cv2.FONT_HERSHEY_DUPLEX, 1, 2
        self.is_dragging = False                            # ドラッグ初期値

        cv2.namedWindow(self.winname)
        cv2.setMouseCallback(self.winname, self.mouse_drag)

        # 以下は必須ではない
        self.image0 = self.images[0]
        self.image0name = self.titles[0]
        cv2.namedWindow(self.image0name)
        self.show_image0()


    def show(self):
        x0, y0 = self.x0, self.y0                           # よく使うので短い変数名とする
        x1, y1, x2, y2 = self.get_roi()                    # 左上座標、右上座標
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        for i, (title, image) in enumerate(zip(self.titles, self.images)):
            roi = np.zeros((self.roiH, self.roiW, 3), np.uint8)

            # 一部画面外にも対応（完全に画面外なら何もしない）
            if (-self.roiW< x0 < self.imgW) and (-self.roiH < y0 < self.imgH):
                tmp = image[y1:y2, x1:x2]
                roi[y1-y0:y2-y0, x1-x0:x2-x0] = tmp

            roi = cv2.resize(roi, (self.WINW, self.WINH))
            self.screen[0:self.WINH, i*self.WINW:(i+1)*self.WINW] = roi

            (w, h), b = cv2.getTextSize(title, self.fontFace, self.fontScale, self.thickness)
            x, y = int((i+0.5)*self.WINW)-w//2, h+b+5
            cv2.putText(self.screen, title, (x, y), self.fontFace, self.fontScale, color, self.thickness)
            cv2.imshow(self.winname, self.screen)


    def show_image0(self):
        img = self.image0.copy()
        cv2.rectangle(img, (self.x0,self.y0), (self.x0+self.roiW ,self.y0+self.roiH),
                        (0,0,255), 2)
        cv2.imshow(self.image0name, img)


    def mouse_drag(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN and not self.is_dragging:
            self.is_dragging = True
            self.ix, self.iy = x, y     # ドラッグ開始時のマウス座標を覚えておく
        
        elif event == cv2.EVENT_MOUSEMOVE and self.is_dragging:
            self.x0 -= x - self.ix
            self.y0 -= y - self.iy
            self.ix, self.iy = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            self.is_dragging = False
        
        elif event == cv2.EVENT_MOUSEWHEEL:
            self.k = self.k+1 if flags > 0 else self.k-1                # ステップ +1もしくは-1する
            bai = self.BAI**self.k                                      # 実際の倍率

            # 現ROIの中心座標（拡大縮小後も同じになるようにする）
            xc = self.x0 + self.roiH//2
            yc = self.y0 + self.roiW//2

            # 新ROIのサイズ　拡大するとROIは小さくなる　縮小するとROIは大きくなる
            self.roiW = int(self.WINW/bai)
            self.roiH = int(self.WINH/bai)

            # 新ROIの左上座標
            self.x0 = xc - self.roiW//2
            self.y0 = yc - self.roiH//2

            self.show_image0()

        elif event == cv2.EVENT_MBUTTONDBLCLK:
            self.ix, self.iy = x % self.WINW, y
            self.k = 0


    def get_roi(self):
        x1, y1 = max(self.x0, 0), max(self.y0,0)
        x2, y2 = min(self.x0+self.roiW, self.imgW), min(self.y0+self.roiH, self.imgH)
        return x1, y1, x2, y2


if __name__ == "__main__":
    pics = {"left": "left.png",
            "right": "right.png"}

    viewer = Viewer(pics)

    while True:
        viewer.show()
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        
    cv2.destroyAllWindows()
