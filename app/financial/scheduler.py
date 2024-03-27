from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.financial.indices_data_loader import indices_data_loader
from app.financial.tickers_data_loader import tickers_data_loader


class Scheduler:
    scheduler: BackgroundScheduler

    def __init__(self):
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.add_job(tickers_data_loader, 'interval', minutes=10)
        self.scheduler.add_job(indices_data_loader, 'interval', hours=1)

    def start(self):
        self.scheduler.start()
