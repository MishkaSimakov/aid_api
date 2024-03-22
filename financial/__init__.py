import math
import requests
from datetime import datetime, timedelta, date
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass


class StockDataInterval(Enum):
    MINUTE = 1
    TEN_MINUTES = 10
    HOUR = 60
    DAY = 24
    WEEK = 7
    MONTH = 31
    QUARTER = 4


@dataclass
class Candle:
    open: float
    close: float
    high: float
    low: float
    value: float
    volume: float
    begin: datetime
    end: datetime

    @staticmethod
    def from_array(data: list) -> 'Candle':
        return Candle(data[0], data[1], data[2], data[3], data[4], data[5], datetime.fromisoformat(data[6]),
                      datetime.fromisoformat(data[7]))


@dataclass
class TickerDividends:
    value: float
    close_date: datetime

    @staticmethod
    def from_array(data: list) -> 'TickerDividends':
        return TickerDividends(data[3], datetime.fromisoformat(data[2]))


def select_data_points(data: list, points: int = 30):
    if not data:
        return []
    if len(data) < points:
        return data
    if points == 1:
        return data[0]

    step = len(data) / points

    return [data[math.ceil(step * i)] for i in range(points)]


class MoexAPI:
    base_url = "https://iss.moex.com/iss"

    def get_tickers(self) -> Optional[list[str]]:
        url = f"statistics/engines/stock/markets/index/analytics/IMOEX/tickers.json"
        return [x[0] for x in self.request_with_retry(url)["tickers"]["data"]]

    def get_ticker_info(self, ticker: str) -> Optional[list]:
        url = f"securities/{ticker}.json"
        data = self.request_with_retry(url)["description"]["data"]

        return data

    def get_last_day_candles(self, ticker: str) -> list[Candle]:
        end_date = datetime.now()
        start_date = (end_date - timedelta(days=1)).replace(hour=0, minute=0, second=0)

        return self.get_candles(ticker, start_date, end_date, StockDataInterval.DAY)

    def get_candles(self, ticker: str, start_date: datetime, end_date: datetime, interval: StockDataInterval,
                    count: int = -1) \
            -> Optional[list[Candle]]:
        url = f"engines/stock/markets/shares/boards/TQBR/securities/{ticker}/candles.json"
        params = {
            'from': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'till': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            'interval': interval.value,
        }

        data = self.request_with_retry(url, params)
        if not data:
            return None

        candles = data["candles"]["data"]

        if count != -1:
            candles = select_data_points(candles, count)

        return list(map(Candle.from_array, candles))

    def get_dividends(self, ticker: str, period: timedelta) -> Optional[list[TickerDividends]]:
        url = f"securities/{ticker}/dividends.json"
        data = self.request_with_retry(url)

        if not data:
            return None

        dividends = map(TickerDividends.from_array, data["dividends"]["data"])

        end_date = datetime.now()
        start_date = end_date - period
        dividends = filter(lambda dividend: start_date <= dividend.close_date <= end_date, dividends)

        return list(dividends)

    def request_with_retry(self, url: str, params: Optional[Dict[str, str]] = None, retry_count: int = 3):
        print("Requesting: " + url)
        if params is None:
            params = {}

        attempt_count = 0
        while attempt_count < retry_count:
            response = requests.get(f"{self.base_url}/{url}", params=params)

            if response.status_code == 200:
                return response.json()

            attempt_count += 1
