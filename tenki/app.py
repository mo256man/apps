from flask import Flask, render_template, request
from getTenki import *
from camera import *

app = Flask(__name__)
camera = Camera()

@app.route("/")
def index():
    return render_template("temperature.html")

@app.route("/getCurrentTenki", methods=["POST"])
def getCurrentTenki():
    if request.method == "POST":
        tenki = get_tenki()
        json2db(tenki)
        daily_tenki = get_daily_tenki()
    return daily_tenki

@app.route("/getDailyTenki", methods=["POST"])
def getDailyTenki():
    if request.method == "POST":
        date = request.form["date"]
        daily_tenki = get_daily_tenki(date)
    return daily_tenki


@app.route("/getCamera", methods=["POST"])
def getCamera():
    if request.method == "POST":
        images = camera.read_data()
    return images

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)