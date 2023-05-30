# pip install py-feat
from feat import Detector
import numpy as np
import cv2

detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model='xgb', # ['svm', 'logistic', 'jaanet']
    emotion_model="resmasknet",
)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord(" "):
            cv2.imwrite("image.jpg", frame)
            break


# single_face_prediction = detector.detect_image("single_face.jpg")
# single_face_prediction = detector.detect_image("woman.jpg", outputFname = "output.csv")
single_face_prediction = detector.detect_image("image.jpg")

print(single_face_prediction.facebox)
print(single_face_prediction.aus)
print(single_face_prediction.emotions)
print(single_face_prediction.facepose) # (in degrees)
figs = single_face_prediction.plot_detections()
print(len(figs)) # 1

figs[0].canvas.draw()
image = np.array(figs[0].canvas.renderer.buffer_rgba())
# image = np.array(figs[0].canvas.renderer._renderer)
image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

cv2.imshow("image", image)
cv2.waitKey(0)
