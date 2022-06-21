from flask import Flask, render_template
from getTenki import *

app = Flask(__name__)

@app.route("/")
def temperature():
    return render_template("temperature.html")

@app.route("/ajax", methods=["POST", "GET"])
def ajax():
    data = json2db()
    print(data)
    return data

if __name__ == "__main__":
    app.run(debug=True)