from typing import Optional
from moex_api import MoexAPI
from datetime import timedelta


class FinancialCalculator:
    ticker: str

    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_return(self) -> Optional[float]:
        ticker_data = MoexAPI().get_last_day_candles(self.ticker)

        if len(ticker_data) == 0:
            return None

        curr_day = ticker_data[-1]
        prev_day = ticker_data[0]

        return curr_day.close / prev_day.close - 1

    def get_dividends(self) -> float:
        dividends = MoexAPI().get_dividends(self.ticker, timedelta(days=365))

        return sum(map(lambda d: d.value, dividends))
