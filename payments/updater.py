from apscheduler.schedulers.background import BackgroundScheduler
from .payment_updater import update_payment


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_payment, 'cron', day=26)
    scheduler.start()