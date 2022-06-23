from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    print("called!")
    return datetime.datetime.now().strftime("%H:%M:%S")

sched = BackgroundScheduler(daemon=True)
sched.add_job(home,'interval',minutes=1) 
sched.start()

if __name__== "__main__":
    app.run(debug=True)