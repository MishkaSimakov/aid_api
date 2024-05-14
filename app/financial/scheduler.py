from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.financial.cachable_data_sources.DataSourcesContainer import DataSourcesContainer


class Scheduler:
    """
    Этот класс отвечает за фоновое обновление данных о тикерах и индексах для главной страницы.
    Он делает это незаметно для пользователя с определённой частотой.
    """

    scheduler: BackgroundScheduler

    def __init__(self):
        """Настраивает BackgroundScheduler."""

        start = datetime.now() + timedelta(seconds=10)

        tickers_source = DataSourcesContainer.tickers_data_source
        indices_source = DataSourcesContainer.indices_data_source

        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.add_job(
            tickers_source.load_from_server_and_cache,
            'interval',
            minutes=10, start_date=start
        )

        self.scheduler.add_job(
            indices_source.load_from_server_and_cache,
            'interval',
            hours=1, start_date=start
        )

    def start(self):
        """Запускает обновление данных о тикерах и индексах."""

        self.scheduler.start()
