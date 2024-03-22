from dataclasses import dataclass

from financial import Candle, MoexAPI, StockDataInterval
from datetime import *
import pandas as pd
from typing import Optional
from functools import wraps


def assure_candles_loaded(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        ticker: 'Ticker' = args[0]

        if ticker.daily_candles is None:
            ticker.load_daily_candles()

        if len(ticker.daily_candles) == 0:
            return None

        return function(*args, **kwargs)

    return wrapper


class Ticker:
    name: str
    daily_candles: Optional[list[Candle]]
    categories_list = {}

    def __init__(self, name: str):
        self.name = name
        self.daily_candles = None

    def get_full_name(self) -> str:
        data = MoexAPI().get_ticker_info(self.name)
        return data[1][2]

    def load_daily_candles(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        self.daily_candles = MoexAPI().get_candles(self.name, start_date, end_date, StockDataInterval.DAY)

    @assure_candles_loaded
    def moving_average(self, window: int) -> float:
        return pd.Series(map(lambda candle: candle.close, self.daily_candles)).rolling(window=window).mean().iloc[-1]

    @assure_candles_loaded
    def exponential_moving_average(self, window: int) -> float:
        return pd.Series(map(lambda candle: candle.close, self.daily_candles)).ewm(span=window).mean().iloc[-1]

    @assure_candles_loaded
    def get_return(self) -> Optional[float]:
        curr_day = self.daily_candles[-1]
        prev_day = self.daily_candles[-2]

        if curr_day.begin.date() != date.today() or prev_day.begin.date() != date.today() - timedelta(days=1):
            return None

        return curr_day.close / prev_day.close - 1

    def get_dividends(self):
        dividends = MoexAPI().get_dividends(self.name, timedelta(days=365))
        return sum(map(lambda d: d.value, dividends))

    @assure_candles_loaded
    def get_relative_dividends(self):
        dividends = MoexAPI().get_dividends(self.name, timedelta(days=365))
        dividends_sum = sum(map(lambda d: d.value, dividends))

        # candles start must be close to dividends period start
        if abs((datetime.now() - self.daily_candles[0].begin).days - 365) > 10:
            return None

        return dividends_sum / self.daily_candles[0].open

    def __repr__(self):
        return f"Ticker(name={self.name})"


if not Ticker.categories_list:
    Ticker.categories_list = {
        "return": {
            "calculator": lambda ticker: ticker.get_return(),
            "postfix": "%"
        },
        "dividends": {
            "calculator": lambda ticker: ticker.get_dividends(),
            "postfix": "₽"
        },
        "relative_dividends": {
            "calculator": lambda ticker: ticker.get_relative_dividends(),
            "postfix": "%"
        }
    }

    # default value is used for lambda-capture
    # for more read: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
    averages_periods = [5, 10, 20, 50, 100, 200]
    for period in averages_periods:
        Ticker.categories_list["ma" + str(period)] = {
            "calculator": (lambda ticker, window=period: ticker.moving_average(window)),
            "postfix": "₽",
        }

    for period in averages_periods:
        Ticker.categories_list["ema" + str(period)] = {
            "calculator": (lambda ticker, window=period: ticker.exponential_moving_average(window)),
            "postfix": "₽",
        }
