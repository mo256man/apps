from feat import Detector
import cv2
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

camH, camW = 720, 1280
frameH, frameW = camH, camH
imgH, imgW = 800, 1200

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, camW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camH)

is_mirror = True
ini_timer = 3
cam_status = 0  # 0:wautubg, 1:countdown, 2:shoot

def getEmote(filename):
    single_face_prediction = detector.detect_image(filename)
    #print(single_face_prediction.facebox)
    #print(single_face_prediction.aus)
    print(single_face_prediction.emotions)
    #print(single_face_prediction.facepose) # (in degrees)
    #figs = single_face_prediction.plot_detections()
    #print(len(figs)) # 1

    #figs[0].canvas.draw()
    #result_img = np.array(figs[0].canvas.renderer.buffer_rgba())
    # image = np.array(figs[0].canvas.renderer._renderer)
    #result_img = cv2.cvtColor(result_img, cv2.COLOR_RGBA2BGR)
    #cv2.imwrite("result.png", result_img)
    return single_face_prediction.emotions.emotions.values.tolist()[0]

def cv2_putText(img, text, org, fontFace, fontScale, color, mode=0):
# cv2.putText()にないオリジナル引数「mode」　orgで指定した座標の基準
# 0（デフォ）＝cv2.putText()と同じく左下　1＝左上　2＝中央

    # テキスト描写域を取得
    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0,0)))
    bbox = dummy_draw.multiline_textbbox((0, 0), text, font=fontPIL)
    _, _, text_w, text_h = bbox
#    text_w, text_h = dummy_draw.textsize(text, font=fontPIL)
#    text_b = int(0.1 * text_h) # バグにより下にはみ出る分の対策

    # テキスト描写域の左上座標を取得（元画像の左上を原点とする）
    x, y = org
    offset_x = [0, 0, text_w//2]
    offset_y = [text_h, 0, text_h//2]
    x0 = x - offset_x[mode]
    y0 = y - offset_y[mode]
    img_h, img_w = img.shape[:2]

    # 画面外なら何もしない
    if not ((-text_w < x0 < img_w) and (-text_h < y0 < img_h)) :
        print ("out of bounds")
        return img

    # テキスト描写域の中で元画像がある領域の左上と右下（元画像の左上を原点とする）
    x1, y1 = max(x0, 0), max(y0, 0)
    x2, y2 = min(x0+text_w, img_w), min(y0+text_h, img_h)

    # テキスト描写域と同サイズの黒画像を作り、それの全部もしくは一部に元画像を貼る
    text_area = np.full((text_h,text_w,3), (0,0,0), dtype=np.uint8)
    text_area[y1-y0:y2-y0, x1-x0:x2-x0] = img[y1:y2, x1:x2]

    # それをPIL化し、フォントを指定してテキストを描写する（色変換なし）
    imgPIL = Image.fromarray(text_area)
    draw = ImageDraw.Draw(imgPIL)
    draw.text(xy = (0, 0), text = text, fill = color, font = fontPIL)

    # PIL画像をOpenCV画像に戻す（色変換なし）
    text_area = np.array(imgPIL, dtype = np.uint8)

    # 元画像の該当エリアを、文字が描写されたものに更新する
    img[y1:y2, x1:x2] = text_area[y1-y0:y2-y0, x1-x0:x2-x0]

    return img


detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model='xgb', # ['svm', 'logistic', 'jaanet']
    emotion_model="resmasknet",
)

# https://github.com/opencv/opencv/tree/master/data/haarcascades　からカスケードファイルを入手する
cascade_path = "./models/haarcascade_frontalface_alt2.xml"
cascade = cv2.CascadeClassifier(cascade_path)

canvas_origin = np.full((imgH,imgW,3), (255,255,255), np.uint8)
canvas_origin = cv2_putText(canvas_origin, "感情メーター", (800,10), "BIZ-UDGothicR.ttc", 50, (0,0,0), 1)
canvas_origin = cv2_putText(canvas_origin, "Py-Feat: Python Facial Expression Analysis Toolbox", (780,70), "BIZ-UDGothicR.ttc", 15, (0,0,255), 1)
words = ["怒り", "嫌悪", "恐り", "幸せ", "悲しみ", "驚き", "自然"]
for i, word in enumerate(words):
    canvas_origin = cv2_putText(canvas_origin, word, (800,i*80+200), "BIZ-UDGothicR.ttc", 30, (0,0,0), 1)

while True:
    canvas = canvas_origin.copy()
    ret, frame = cap.read()
    if ret:
        if is_mirror:
            frame = frame[:, (camW-frameW)//2:(camW+frameW)//2, :]
            frame = cv2.flip(frame, 1)      # 左右反転
            image = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray)

        if len(faces) > 0:
            areas = [w*h for _, _, w, h in faces]
            max_area_index = areas.index(max(areas))
            x, y, w, h = faces[max_area_index]
            image = cv2.rectangle(img=image, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)
            
        if cam_status == 1:
            timer = start_time + ini_timer - time.time()
            if timer < 0:
                cam_status = 2
                continue
            else:
                endAngle = (timer - int(timer)) * 360      # 角度
                text = str(int(timer))
                fontFace = cv2.FONT_HERSHEY_DUPLEX
                fontScale = 4
                thickness = 10
                (w, h), _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
                cv2.ellipse(image, (frameW//2,frameH//2), (100,100), 0, -90, endAngle-90, (255,255,255), thickness=10)
                cv2.putText(image, text, ((frameW-w)//2,(frameH+h)//2), fontFace, fontScale, (255,255,255), thickness)

        canvas[40:40+frameH, 40:40+frameW] = image

        if cam_status == 2:
            canvas = canvas_origin.copy()
            text = "processing..."
            fontScale = 3
            thickness = 2
            (w, h), _ = cv2.getTextSize(text, fontFace, fontScale, thickness)
            cv2.putText(image, text, ((frameW-w)//2,(frameH+h)//2), fontFace, fontScale, (255,255,255), thickness)
            cv2.imwrite("photo.jpg", frame)
            canvas[40:40+frameH, 40:40+frameW] = image
            cv2.imshow("" ,canvas)
            cv2.waitKey(1)
            emotions = getEmote("photo.jpg")
            for i, value in enumerate(emotions):
                x, y = 900, i*80+200
                width = 280
                cv2.rectangle(canvas, (x,y), (x+int(width*value),y+40), (200,200,0), -1)
                cv2.putText(canvas, f"{int(value*100)}%", (x+20,y+20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 1)
            cam_status = 0

        cv2.imshow("" ,canvas)
        key = cv2.waitKey(1)
        if key == 27:
            break
        elif key == ord(" "):
            if cam_status == 0:
                cam_status = 1
                start_time = time.time()
    else:
        break

