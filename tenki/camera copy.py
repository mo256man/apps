import cv2
import numpy as np
from datetime import datetime
import csv
import random
from cv2 import aruco
from segment import *
import pandas as pd

class Camera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.w = 640
        self.h = 480
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
        self.margin = 50
        self.then = datetime.now()                                  # 仮に、現在日時
        self.now = datetime.now()                                   # 現在日時
        self.lastimage = np.zeros((self.h, self.w, 4), np.uint8)    # 1フレーム前の画像の初期値
        self.base = np.full((self.h, 2*self.w+self.margin, 4), (0,0,0,0), np.uint8)    # 二つの画像を隙間を開けて合体するベース
        self.path = ".\\static\\"

        df = pd.read_csv(self.path + "data.csv", sep=",")           # データフレームでcsvを取り込む
        last_data = df.tail(1).values.tolist()[0]                   # といっても欲しいのは最後の1行のみ
        _, self.last_co2, self.last_temp, self.last_hum = last_data # 直前のCO2濃度と温度と湿度を覚えておく

    def read_data(self):
        ret, frame = self.video.read()                                  # カメラ映像を取得する
        if ret:                                                         # 正しく撮れていたら
            cv2.imwrite(self.path + "photo.jpg", frame)                 # 画像を保存する
            self.lastimage = frame                                      # これを直近の画像として覚えておく
        else:                                                           # 正しく撮れていなかったら
            frame = self.lastimage                                      # 直近の画像を思い出す
        
        # 画像処理1 ArUcoマーカーで矩形を取得する
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                  # グレースケールにする
        corners, ids = detectMarkers(gray)                              # マーカーを検出する
        image1 = aruco.drawDetectedMarkers(frame.copy(), corners, ids)  # マーカー検出結果を描写する
        cv2.imwrite(self.path + "image1.jpg", image1)                   # 以上の加工をした画像を保存する
        self.image1 = image1

        # 画像処理2 ArUcoマーカーで矩形を取得する
        if len(corners) == 4:                                           # マーカーが4個ならば
            dic_id = {}
            for i, id in enumerate(np.ravel(ids)):                      # idsは扱いづらいかたちなので一次元にして
                dic_id[id] = i                                          # 何番目のマークのidが何なのかを辞書にする
            pos0 = corners[dic_id[0]][0][3]                             # 左上
            pos1 = corners[dic_id[1]][0][3]                             # 右上
            pos2 = corners[dic_id[2]][0][3]                             # 右下
            pos3 = corners[dic_id[3]][0][3]                             # 左下
            pts1 = np.float32([pos0, pos1, pos2, pos3])                 # カメラ映像の中のマーカーの座標群
            pts2 = np.float32([(0,0), (900,0), (900,300), (0,300)])     # CO2計のサイズが90*270なので仮にこのサイズにする
            M = cv2.getPerspectiveTransform(pts1, pts2)                 # 投影行列
            rect = cv2.warpPerspective(frame, M, (900,300))             # 不等辺四角形を長方形に変形する
            bai = self.w / rect.shape[1]                                # 幅をカメラ映像の幅に拡大する倍率
            image2 = cv2.resize(rect.copy(), None, fx=bai, fy=bai)      # カメラ映像のサイズに拡大縮小する
            cv2.imwrite(self.path + "image2.jpg", image2)               # 以上の加工をした画像を保存する

        # ここからが本番　7セグを読み取る
            str_now = datetime.now().strftime("%Y-%m-%d %H:%M")             # 現在時刻を文字列にする
            value_co2, value_temp, value_hum = read_values(rect)       # CO2計を読み取る
            print(value_co2, value_temp, value_hum)
            if value_co2:                                               # CO2濃度がTrue（数値）ならば
                self.last_co2 = value_co2                             # それを直近の値として覚えておく
            else:                                                       # Falseならば
                value_co2 = self.last_co2                             # 直近の値を思い出す

            if value_temp:
                self.last_temp = value_temp
            else:
                value_temp = self.last_temp

            if value_hum:
                self.last_hum = value_hum
            else:
                value_hum = self.last_hum

            row = [str_now, value_co2, value_temp, value_hum]           # csvに書き込む1行分のデータ
            print(row)
            print()
            
            with open(".\\static\\data.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)


def detectMarkers(gray):
    dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)                # 事前登録されているマーカーの辞書
    parameters = aruco.DetectorParameters_create()                      # パラメータ自動決定
    corners, ids, _ = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)
    return corners, ids

def main():
    cam = Camera()

    while True:
        cam.read_data()
        cv2.imshow("", cam.image1)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

if __name__ == "__main__":
    main()