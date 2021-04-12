from flask import Flask
from flask_apscheduler import APScheduler
import google_drive_service as drive
import gmail_service as gmail
import scheduler as scheduler
import spreadsheet_service as spreadsheet

app = Flask(__name__)
apsscheduler = APScheduler()


@app.route("/")
def index():
    return "Welcome to the scheduler!"


def scheduled_task():
    # get data from google drive
    data_file = drive.get_data_file()
    # read lines and split each one by ','
    lines = [item.strip().split(',') for item in data_file.split('\n')]
    #  create scheduler
    result_data = scheduler.data_processing(lines[1:])
    # create spreadsheet
    spreadsheet.create(result_data)
    # send email with spreadsheet attached, path= utils/
    gmail.send()


def counter():
    print("1")


if __name__ == '__main__':
    # apsscheduler.add_job(id='Scheduled task', func=scheduled_task, trigger='cron', day_of_week=0)
    apsscheduler.add_job(id='Scheduled task', func=scheduled_task, trigger='interval', seconds = 60)
    apsscheduler.start()
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=False)
