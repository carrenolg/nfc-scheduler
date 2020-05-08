from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

count = 0

def sensor():
    global count
    sched.print_jobs()
    print('Count: ', count)
    count += 1


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, 'cron', minute='*')
sched.start()

@app.route("/")
def hello():
    return "Hello, Marlene!" + str(count)

if __name__ == '__main__':
    app.run(debug=True)