from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.financial.indices_data_loader import indices_data_loader
from app.financial.tickers_data_loader import tickers_data_loader


class Scheduler:
    scheduler: BackgroundScheduler

    def __init__(self):
        start = datetime.now() + timedelta(seconds=10)

        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.add_job(tickers_data_loader, 'interval', minutes=10, start_date=start)
        self.scheduler.add_job(indices_data_loader, 'interval', hours=1, start_date=start)

    def start(self):
        self.scheduler.start()
