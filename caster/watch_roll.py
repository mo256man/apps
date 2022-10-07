import cv2
import numpy as np
from cv2 import aruco
import math
import time


class Roi():
    def __init__(self):
        self.width = 500
        self.y1 = -100
        self.y2 = 200
        self.height = self.y2 - self.y1
        self.image = np.full((self.height, self.width, 3), 0, np.uint8)
        self.lastimage = self.image.copy()

    def draw(self, frame, x, y):
        """
        マーカーの周囲の画像を取得する
        マーカーが画面の端のほうにあって必要な大きさの周囲画像を取れない場合は取得しない（以前の画像のまま）
        """
        h, w = frame.shape[:2]
        if (self.width//2<=x<=w-self.width//2) and (self.y1 <= y <= h-self.y2):
            self.lastimage = self.image.copy()
            self.image = frame.copy()[y+self.y1:y+self.y2, x-self.width//2:x+self.width//2]
        else:
            self.image = self.lastimage.copy()


"""
四角形検出
https://qiita.com/sitar-harmonics/items/ac584f99043574670cf3
"""
def angle(pt1, pt2, pt0) -> float:
    """
    pt0-> pt1およびpt0-> pt2からの
    ベクトル間の角度の余弦(コサイン)を算出
    """
    dx1 = float(pt1[0,0] - pt0[0,0])
    dy1 = float(pt1[0,1] - pt0[0,1])
    dx2 = float(pt2[0,0] - pt0[0,0])
    dy2 = float(pt2[0,1] - pt0[0,1])
    v = math.sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) )
    return (dx1*dx2 + dy1*dy2)/ v


def find_rect(image, cx, cy, cond_area=1000):
    """
    四角形を検出
    ただしマーカーの四角形（中心がcx,cy）はノーカン
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    points = []

    # 輪郭取得
    contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        # 輪郭の周囲に比例する精度で輪郭を近似する
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, arclen*0.02, True)

        # 凸性の確認
        area = abs(cv2.contourArea(approx))
        if approx.shape[0] == 4 and area > cond_area and cv2.isContourConvex(approx) :
            maxCosine = 0
            for j in range(2, 5):
                # 辺間の角度の最大コサインを算出
                cosine = abs(angle(approx[j%4], approx[j-2], approx[j-1]))
                maxCosine = max(maxCosine, cosine)

            if maxCosine < 0.3 :                                    # 四角判定　角のコサインが全部0.3以下
                rcnt = approx.reshape(-1,2)
                x, y = np.mean(rcnt, axis=0)                        # 各点のxとyの中心（平均値）
                x1, y1 = np.min(rcnt, axis=0)                       # x, yの最小値
                x2, y2 = np.max(rcnt, axis=0)                       # x, yの最大値
#                if True:
                if not((x1<x<x2) and (y1<y<y2)):                    # 四角形がマーカーの四角形とほぼ同じ位置に ない ときは
                    points.append((x,y))
                    cv2.polylines(image, [rcnt], True, (255,0,0), thickness=2)
    return points, image



def find_triangle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("threshold", threshold)

    triangles = 0  # 三角形カウント用
    #抽出した領域を1つずつ取り出し輪郭を近似する。三角形の場合、輪郭を赤くする
    for cnt in contours:
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
#        if True:
        if len(approx) == 3:
            cv2.drawContours(image, [approx], 0, (0, 0, 255), 2)
            triangles += 1

    return image



def main(filename):
    cap = cv2.VideoCapture(filename)
    dic_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    roi = Roi()
    frame_cnt = 0

    while True:
        ret, frame = cap.read()
        if ret:
            w = frame.shape[1]
            show_frame = frame.copy()
            show_frame[:, :roi.width//2] = 0.5 * show_frame[:, :roi.width//2].astype(np.uint8)
            show_frame[:, w-roi.width//2:] = 0.5 * show_frame[:, w-roi.width//2:].astype(np.uint8)
            cv2.putText(frame, f"frame: {frame_cnt}", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = aruco.detectMarkers(gray, dic_aruco)

            if len(corners) > 0:
                aruco.drawDetectedMarkers(show_frame, corners, ids)
                list_ids = np.ravel(ids)                                     # idsを一次元にする
                for corner, id in zip(corners,ids):
                    if id==0:
                        # id==0のとき、基準
                        cv2.putText(show_frame, f"marker is found", (20, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 2)
                        corner = corner.reshape((4,2))                     # cornersをリシェイプする
                        cx, cy = np.mean(corner, axis=0)                       # 各点のxとyの平均値
                        cx, cy = int(cx), int(cy)                               # 整数にする
                        cv2.circle(show_frame, (cx, cy), 3, (0,255,0), 2)
                        roi.draw(frame, cx, cy)

                    else:
                        # id==0でないとき、回転する
                        pass

                wait_time = 100                                           # cv2.imshow()の待ち時間
            else:
                cv2.putText(show_frame, f"marker is not found", (20, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
                wait_time = 100                                           # cv2.imshow()の待ち時間
                roi.image = roi.lastimage

            diff = cv2.absdiff(roi.image, roi.lastimage)
            # diff = find_triangle(diff)
            cv2.imshow("frame", show_frame)
            cv2.imshow("diff", diff)
            cv2.imshow("roi", roi.image)
            key = cv2.waitKey(wait_time)
            frame_cnt += 1

            if key & 0xFF == 27:
                break

        else:
            time.sleep(2)   # sec
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    filename = "caster_2.mp4"
    main(filename)
