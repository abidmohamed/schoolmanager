from apscheduler.schedulers.background import BackgroundScheduler
from .attendance_update import update_attendance
# import schedule
import time


def start():
    # schedule.every().day.at("12:50").do(update_something)
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_attendance, 'cron', hour=7)
    scheduler.start()
