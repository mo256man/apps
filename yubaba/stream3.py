from flask import Flask, render_template, Response, request
import cv2
import json
import base64
import datetime

app = Flask(__name__)

class Camera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def read(self):
        _, frame = self.video.read()
        return frame

def mosaic(image):
    h, w = image.shape[:2]
    image = cv2.resize(image, (w//10, h//10))
    image = cv2.resize(image, (w,h), interpolation=cv2.INTER_NEAREST)
    return image

def img2base64(image):
    _, imgEnc = cv2.imencode(".jpg", image)
    imgB64 = base64.b64encode(imgEnc)
    strB64 = "data:image/jpg;base64," + str(imgB64, "utf-8")
    return strB64

@app.route("/")
def stream():
    return render_template("stream3.html")

@app.route("/call_from_ajax", methods = ["POST"])
def callfromajax():
    if request.method == "POST":
        image1 = camera.read()
        str_img1 = img2base64(image1)
        image2 = mosaic(image1)
        str_img2 = img2base64(image2)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        dict = {"image1": str_img1,
                "image2": str_img2,
                "now": now}
    return json.dumps(dict)

if __name__ == "__main__":
    camera = Camera()
    app.run(debug=True)