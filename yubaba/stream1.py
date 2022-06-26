from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

class Camera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def read(self):
        while True:
            _, frame = self.video.read()
            # 必要ならここで画像処理する
            yield frame

@app.route("/")
def stream():
    return render_template("stream1.html")

@app.route("/video")
def video():
    frame = camera.read()
    _, encoded = cv2.imencode(".jpg", frame)
    bin = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + encoded.tobytes() + b"\r\n"
    return Response(bin,
            mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    camera = Camera()
    app.run(debug=True)