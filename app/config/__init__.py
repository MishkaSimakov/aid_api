from datetime import timedelta
from app.financial import StockDataInterval


class ChartConfig:
    periods = {
        "1H": {
            "delta": timedelta(hours=1),
            "interval": StockDataInterval.MINUTE
        },
        "1D": {
            "delta": timedelta(days=1),
            "interval": StockDataInterval.TEN_MINUTES
        },
        "1W": {
            "delta": timedelta(days=7),
            "interval": StockDataInterval.HOUR
        },
        "1M": {
            "delta": timedelta(days=30),
            "interval": StockDataInterval.HOUR
        },
        "1Y": {
            "delta": timedelta(days=365),
            "interval": StockDataInterval.WEEK
        },
        "ALL": {
            "delta": timedelta(days=365 * 100),
            "interval": StockDataInterval.MONTH
        }
    }
