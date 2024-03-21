from typing import Callable
from finance_calculations import percentage
from datetime import timedelta
from moex_api import StockDataInterval

class Category:
    postfix: str
    calculator: Callable[[str], float]

    def __init__(self, postfix: str, calculator: Callable[[str], float]):
        self.postfix = postfix
        self.calculator = calculator


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
        "1M": {
            "delta": timedelta(days=30),
            "interval": StockDataInterval.DAY
        },
        "1Y": {
            "delta": timedelta(days=365),
            "interval": StockDataInterval.WEEK
        }
    }


class CategoriesConfig:
    categories = {
        "return": Category("%", percentage.calculate_return)
    }
