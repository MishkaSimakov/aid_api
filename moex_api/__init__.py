import apimoex
import requests
from datetime import datetime, timedelta
from enum import Enum


class StockDataInterval(Enum):
    MINUTE = 1
    TEN_MINUTES = 10
    HOUR = 60
    DAY = 24
    WEEK = 7
    MONTH = 31
    QUARTER = 4


class MoexAPI:
    base_url = "https://iss.moex.com/iss"

    def get_tickers(self):
        url = f"{self.base_url}/statistics/engines/stock/markets/index/analytics/IMOEX/tickers.json"

        response = requests.get(url)
        if response.status_code != 200:
            return None

        data = response.json()["tickers"]["data"]

        return [x[0] for x in data]

    def get_last_data_for_ticker(self, ticker):
        url = f"{self.base_url}/engines/stock/markets/shares/boards/TQBR/securities/{ticker}/candles.json"

        params = {
            'from': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'till': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
            'interval': StockDataInterval.HOUR.value,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None

        data = response.json()["candles"]["data"]

        return data

    def get_stock_data(self, ticker, start_date, end_date, interval):
        url = f"{self.base_url}/engines/stock/markets/shares/boards/TQBR/securities/{ticker}/candles.json"
        params = {
            'from': start_date,
            'till': end_date,
            'interval': interval,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['candles']['data']
        else:
            return None

    def select_data_points(self, data, points=30):
        if not data or len(data) < points:
            return []
        step = len(data) // points
        return [data[i][1] for i in range(0, len(data), step)]

    def main(self, ticker: str, delta: timedelta, interval: StockDataInterval):
        till_time = datetime.now()
        from_time = till_time - delta

        last_hour_data = self.get_stock_data(ticker, from_time.strftime('%Y-%m-%d %H:%M:%S'),
                                             till_time.strftime('%Y-%m-%d %H:%M:%S'), interval)
        last_hour_points = self.select_data_points(last_hour_data)

        result = {
            "1H": last_hour_points,
        }

        return result

    def get_tickers_list(self):
        index_id = 'IMOEX'

        with requests.Session() as session:
            data = apimoex.get_index_tickers(session, index_id)

        return [x["ticker"] for x in data]

    def get_return_for_ticker(self, ticker: str):
        with requests.Session() as session:
            data = apimoex.get_market_candles(session, ticker, 1)

        return data
