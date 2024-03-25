from datetime import timedelta
from app.financial import StockDataInterval


class ChartConfig:
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
    last_data_path = "storage/last_data"
    images_path = "storage/images"
    log_path = "storage/debug.log"
