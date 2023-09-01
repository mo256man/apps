from flask import Flask, render_template, request
from koyomi import Ephem
app = Flask(__name__)
my_ephem = Ephem()

@app.route("/")
def index():
    return render_template("index.html", ephem = my_ephem)

@app.route("/date_minus")
def date_minus():
    my_ephem.change_date(-1)
    return render_template("index.html", ephem = my_ephem)

@app.route("/date_today")
def date_today():
    my_ephem.change_date(0)
    return render_template("index.html", ephem = my_ephem)

@app.route("/date_plus")
def date_plus():
    my_ephem.change_date(1)
    return render_template("index.html", ephem = my_ephem)

if __name__ == "__main__":
    app.run(debug=True)