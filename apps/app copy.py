from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request, redirect
from app_base64 import img2base64
from app_hanko import Make_Hanko
app = Flask(__name__)


def get_attribue(att_name, default_value):
    try:
        value = request.form[att_name]      # これで得られるのは数字であっても文字列
        if default_value.isdecimal():       # デフォルト値が数値ならば
            value = int(value)              # 整数にする
    except:                                 # request.form[] で値が得られなかった場合
        value = default_value               # 事前に設定したデフォルト値とする
    return value


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hanko", methods=["get", "post"])
def hanko():
    text = get_attribue("text", "")                         # 辞書でなくクラスにすること
    width = get_attribue("width", 200)
    height = get_attribue("height", 200)
    radius = get_attribue("radius", 20)
    thickness = get_attribue("thickness", 10)
    dict = {"text": get_attribue("text", ""),
            "width": get_attribue("width", 200),
            "height": get_attribue("height", 200),
            "radius": get_attribue("radius", 20),
            "thickness": get_attribue("thickness", 10),
            }
    hanko = Make_Hanko(dict)
    return render_template("hanko.html", hanko=hanko)

if __name__ == "__main__":
    app.run(debug=True)
