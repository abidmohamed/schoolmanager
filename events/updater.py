from apscheduler.schedulers.background import BackgroundScheduler
from .event_update import update_event
# import schedule
import time


def start():
    # schedule.every().day.at("12:50").do(update_something)
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_event, 'cron', day=1)
    scheduler.start()
