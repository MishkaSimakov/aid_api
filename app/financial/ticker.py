from app.financial import Candle, MoexAPI, StockDataInterval
from datetime import *
import pandas as pd
from typing import Optional, Callable, Dict
from functools import wraps
from technical_analysis import indicators
from dataclasses import asdict
from dataclasses import dataclass


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


@dataclass
class IndicatorCalculatorResponse:
    value: float
    verdict: float


@dataclass
class TickerIndicator:
    calculator: Callable[['Ticker'], IndicatorCalculatorResponse]
    description: str
    postfix: str

    def calculate_for_ticker(self, ticker: 'Ticker') -> dict:
        result = self.calculator(ticker)
        return {
            "value": result.value if result is not None else None,
            "postfix": self.postfix,
            "description": self.description,
            "verdict": result.verdict if result is not None else None
        }


class Ticker:
    name: str
    daily_candles: Optional[list[Candle]]
    candles_dataframe: pd.DataFrame
    categories_list: Dict[str, TickerIndicator] = {}

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
        self.candles_dataframe = pd.DataFrame.from_records([asdict(candle) for candle in self.daily_candles])

    @assure_candles_loaded
    def moving_average(self, window: int) -> Optional[IndicatorCalculatorResponse]:
        return IndicatorCalculatorResponse(
            value=pd.Series(self.candles_dataframe.close).rolling(window=window).mean().iloc[-1],
            verdict=0
        )

    @assure_candles_loaded
    def exponential_moving_average(self, window: int) -> Optional[IndicatorCalculatorResponse]:
        return IndicatorCalculatorResponse(
            value=pd.Series(self.candles_dataframe.close).ewm(span=window).mean().iloc[-1],
            verdict=0,
        )

    @assure_candles_loaded
    def get_profitability(self) -> Optional[IndicatorCalculatorResponse]:
        curr_day = self.daily_candles[-1]
        prev_day = self.daily_candles[-2]

        if curr_day.begin.date() != date.today() or prev_day.begin.date() != date.today() - timedelta(days=1):
            return None

        return IndicatorCalculatorResponse(
            value=curr_day.close / prev_day.close - 1,
            verdict=0,
        )

    @assure_candles_loaded
    def indicator_atr(self, window) -> Optional[IndicatorCalculatorResponse]:
        value = indicators.atr(self.candles_dataframe.high, self.candles_dataframe.low, self.candles_dataframe.close,
                               period=window).iloc[-1]
        return IndicatorCalculatorResponse(
            value=value,
            verdict=0,
        )

    @assure_candles_loaded
    def indicator_rsi(self, window) -> Optional[IndicatorCalculatorResponse]:
        value = indicators.rsi(self.candles_dataframe.close, period=window).iloc[-1]
        return IndicatorCalculatorResponse(
            value=value,
            verdict=0
        )

    @assure_candles_loaded
    def indicator_perc_r(self, window) -> Optional[IndicatorCalculatorResponse]:
        value = indicators.perc_r(self.candles_dataframe.high, self.candles_dataframe.low, self.candles_dataframe.close,
                                  period=window).iloc[-1]
        return IndicatorCalculatorResponse(
            value=value,
            verdict=0
        )

    @assure_candles_loaded
    def indicator_trix(self, window) -> Optional[IndicatorCalculatorResponse]:
        value = indicators.trix(self.candles_dataframe.close, period=window).iloc[-1]
        return IndicatorCalculatorResponse(
            value=value,
            verdict=0
        )

    def get_dividends(self) -> Optional[IndicatorCalculatorResponse]:
        dividends = MoexAPI().get_dividends(self.name, timedelta(days=365))
        return IndicatorCalculatorResponse(
            value=sum(map(lambda d: d.value, dividends)),
            verdict=0
        )

    @assure_candles_loaded
    def get_relative_dividends(self) -> Optional[IndicatorCalculatorResponse]:
        dividends = MoexAPI().get_dividends(self.name, timedelta(days=365))
        dividends_sum = sum(map(lambda d: d.value, dividends))

        # candles start must be close to dividends period start
        if abs((datetime.now() - self.daily_candles[0].begin).days - 365) > 10:
            return None

        return IndicatorCalculatorResponse(
            value=dividends_sum / self.daily_candles[0].open,
            verdict=0,
        )

    def __repr__(self):
        return f"Ticker(name={self.name})"


if not Ticker.categories_list:
    # TODO: add descriptions for atr...
    Ticker.categories_list = {
        "profitability": TickerIndicator(
            calculator=lambda ticker: ticker.get_profitability(),
            postfix="%",
            description="Доходность за период"
        ),
        "dividends": TickerIndicator(
            calculator=lambda ticker: ticker.get_dividends(),
            postfix="₽",
            description="Дивиденды за год"
        ),
        "relative_dividends": TickerIndicator(
            calculator=lambda ticker: ticker.get_relative_dividends(),
            postfix="%",
            description="Дивидендная доходность за год"
        ),
        "atr": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_atr(window=10),
            postfix="%",
            description="yet to come"
        ),
        "rsi": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_rsi(window=10),
            postfix="%",
            description="yet to come"
        ),
        "perc_r": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_perc_r(window=10),
            postfix="%",
            description="yet to come"
        ),
        "trix": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_trix(window=10),
            postfix="%",
            description="yet to come"
        )
    }

    # default value is used for lambda-capture
    # for more read: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
    averages_periods = [5, 10, 20, 50, 100, 200]
    for period in averages_periods:
        Ticker.categories_list["ma" + str(period)] = TickerIndicator(
            calculator=(lambda ticker, window=period: ticker.moving_average(window)),
            postfix="₽",
            description=f"Скользящее среднее за {period} дней"
        )

    for period in averages_periods:
        Ticker.categories_list["ema" + str(period)] = TickerIndicator(
            calculator=(lambda ticker, window=period: ticker.exponential_moving_average(window)),
            postfix="₽",
            description=f"Экспоненциальное скользящее среднее за {period} дней"
        )
