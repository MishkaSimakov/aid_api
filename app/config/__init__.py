from datetime import timedelta
from app.financial import StockDataInterval


class ChartConfig:
    """
    Этот класс содержит доступные периоды для графика цен на тикер.
    В запросе приходит ключ (H, M, ...), а значения delta и interval используются
    для составления запроса к Мосбирже
    """

    periods = {
        "H": {
            "delta": timedelta(hours=1),
            "interval": StockDataInterval.MINUTE
        },
        "D": {
            "delta": timedelta(days=1),
            "interval": StockDataInterval.TEN_MINUTES
        },
        "W": {
            "delta": timedelta(days=7),
            "interval": StockDataInterval.HOUR
        },
        "M": {
            "delta": timedelta(days=30),
            "interval": StockDataInterval.HOUR
        },
        "Y": {
            "delta": timedelta(days=365),
            "interval": StockDataInterval.WEEK
        },
        "A": {
            "delta": timedelta(days=365 * 100),
            "interval": StockDataInterval.MONTH
        }
    }


class Paths:
    """Здесь заданы пути, которые используются программой."""

    cache_data_path = "storage/tickers_data"
    images_path = "storage/images"
    log_path = "storage/debug.log"
