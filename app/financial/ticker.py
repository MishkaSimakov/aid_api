from app.financial import Candle, MoexAPI, StockDataInterval
from datetime import *
import pandas as pd
from typing import Optional, Callable, Dict
from functools import wraps
from technical_analysis import indicators
from dataclasses import asdict
from dataclasses import dataclass


def assure_candles_loaded(function):
    """
    Специальный декоратор для функций, которые используют данные о тикере.
    Он проверяет, что данные загружены, а если это не так, то загружает их.
    """

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
    """
    Для каждого тикера существует множество индикаторов - специальных значений,
    которые показывают, стоит ли его покупать или продавать.
    Этот класс хранит результат вычисления такого индикатора.
    """

    value: float
    verdict: Optional[float]  # 1 - покупать, -1 - продавать


@dataclass
class TickerIndicator:
    """
    Хранит в себе данные об индикаторе:
    calculator - функция, которая его вычисляет,
    name - название,
    postfix - постфикс, который должен быть добавлен к численному значению индикатора,
    description - описание индикатора
    """

    calculator: Callable[['Ticker'], IndicatorCalculatorResponse]
    name: str
    postfix: str
    description: str = ""

    def calculate_for_ticker(self, ticker: 'Ticker') -> dict:
        """
        Вычисляет значение индикатора для данного тикера и возвращает его в виде словаря,
        который может быть передан клиенту.
        """

        result = self.calculator(ticker)
        return {
            "value": result.value if result is not None else None,
            "postfix": self.postfix,
            "name": self.name,
            "description": self.description,
            "verdict": result.verdict if result is not None else None
        }


class Ticker:
    """Хранит и загружает данные о тикере."""

    name: str
    lang: str
    daily_candles: Optional[list[Candle]]
    candles_dataframe: pd.DataFrame
    categories_list: Dict[str, TickerIndicator] = {}

    def __init__(self, name: str, lang: str):
        self.name = name
        self.daily_candles = None
        self.lang = lang

    @assure_candles_loaded
    def get_current_price(self) -> float:
        """Возвращает последнюю известную цену на тикер - цену закрытия в последний промежуток времени."""
        return self.daily_candles[-1].close

    def get_names(self) -> (str, str):
        """Возвращает короткое и полное название для тикера."""

        ticker_info = MoexAPI().get_ticker_info(self.name)

        try:
            short_name = ticker_info[2][2]
            full_name = ticker_info[1][2]
        except IndexError as e:
            short_name = self.name
            full_name = self.name

        return short_name, full_name

    @assure_candles_loaded
    def get_value(self) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает оборот по данному тикеру за последний день."""

        curr_day = self.daily_candles[-1]

        return IndicatorCalculatorResponse(
            value=curr_day.value / 1e6,
            verdict=None
        )

    def load_daily_candles(self):
        """
        Загружает данные с api Мосбиржи для данного тикера с интервалом в один день,
        эти данные потом используются для вычисления индикаторов.
        """

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        self.daily_candles = MoexAPI().get_candles(self.name, start_date, end_date, StockDataInterval.DAY)
        self.candles_dataframe = pd.DataFrame.from_records([asdict(candle) for candle in self.daily_candles])

    @assure_candles_loaded
    def moving_average(self, window: int) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает скользящее среднее с окном размера window."""

        value = pd.Series(self.candles_dataframe.close).rolling(window=window).mean().iloc[-1]
        current_price = self.get_current_price()

        verdict = 0
        if value < current_price:
            verdict = 1
        elif value > current_price:
            verdict = -1

        return IndicatorCalculatorResponse(
            value=value,
            verdict=verdict
        )

    @assure_candles_loaded
    def exponential_moving_average(self, window: int) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает экспоненциальное скользящее среднее с окном размера window."""

        value = pd.Series(self.candles_dataframe.close).ewm(span=window).mean().iloc[-1]
        current_price = self.get_current_price()

        verdict = 0
        if value < current_price:
            verdict = 1
        elif value > current_price:
            verdict = -1

        return IndicatorCalculatorResponse(
            value=value,
            verdict=verdict,
        )

    @assure_candles_loaded
    def get_profitability(self) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает доходность тикера за день."""

        curr_day = self.daily_candles[-1]
        prev_day = self.daily_candles[-2]

        if curr_day.begin.date() != date.today() or prev_day.begin.date() != date.today() - timedelta(days=1):
            return None

        return IndicatorCalculatorResponse(
            value=(curr_day.close / prev_day.close - 1) * 100,
            verdict=0,
        )

    @assure_candles_loaded
    def indicator_atr(self, window) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает средний истинный диапазон."""

        value = indicators.atr(self.candles_dataframe.high, self.candles_dataframe.low, self.candles_dataframe.close,
                               period=window).iloc[-1]
        return IndicatorCalculatorResponse(
            value=value,
            verdict=None
        )

    @assure_candles_loaded
    def indicator_rsi(self, window) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает индекс относительной силы."""

        value = indicators.rsi(self.candles_dataframe.close, period=window).iloc[-1]

        verdict = 0
        if value > 60:
            verdict = 1
        elif value < 40:
            verdict = -1

        return IndicatorCalculatorResponse(
            value=value,
            verdict=verdict
        )

    @assure_candles_loaded
    def indicator_perc_r(self, window) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает процентный диапазон Вильямса."""

        value = indicators.perc_r(self.candles_dataframe.high, self.candles_dataframe.low, self.candles_dataframe.close,
                                  period=window).iloc[-1]

        verdict = 0
        if value > 0.6:
            verdict = -1
        elif value < 0.4:
            verdict = 1

        return IndicatorCalculatorResponse(
            value=value * -100,
            verdict=verdict
        )

    @assure_candles_loaded
    def indicator_trix(self, window) -> Optional[IndicatorCalculatorResponse]:
        """Считает импульсный индикатор."""

        value = indicators.trix(self.candles_dataframe.close, period=window).iloc[-1]

        verdict = 0
        if value >= 0.01:
            verdict = -1
        elif value <= -0.01:
            verdict = 1

        return IndicatorCalculatorResponse(
            value=value * 100,
            verdict=verdict
        )

    def get_dividends(self) -> Optional[IndicatorCalculatorResponse]:
        """Возвращает дивиденды по данному тикеру за год."""

        dividends = MoexAPI().get_dividends(self.name, timedelta(days=365))
        return IndicatorCalculatorResponse(
            value=sum(map(lambda d: d.value, dividends)),
            verdict=0
        )

    @assure_candles_loaded
    def get_relative_dividends(self) -> Optional[IndicatorCalculatorResponse]:
        """Индикатор, который возвращает дивиденды относительно цены данного тикера."""

        dividends = MoexAPI().get_dividends(self.name, timedelta(days=365))
        dividends_sum = sum(map(lambda d: d.value, dividends))

        if abs((datetime.now() - self.daily_candles[0].begin).days - 365) > 10:
            return None

        return IndicatorCalculatorResponse(
            value=dividends_sum / self.daily_candles[0].open * 100,
            verdict=0,
        )

    def __repr__(self):
        return f"Ticker(name={self.name})"


if not Ticker.categories_list:
    Ticker.categories_list = {
        "profitability": TickerIndicator(
            calculator=lambda ticker: ticker.get_profitability(),
            postfix="%",
            name="Доходность за день",
        ),
        "abs-div": TickerIndicator(
            calculator=lambda ticker: ticker.get_dividends(),
            postfix="₽",
            name="Дивиденды за год"
        ),
        "rel-div": TickerIndicator(
            calculator=lambda ticker: ticker.get_relative_dividends(),
            postfix="%",
            name="Дивидендная доходность за год"
        ),
        "atr": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_atr(window=10),
            postfix="",
            name="Средний истинный диапазон"
        ),
        "rsi": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_rsi(window=10),
            postfix="%",
            name="Индекс относительной силы"
        ),
        "perc-r": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_perc_r(window=10),
            postfix="%",
            name="Процентный диапазон Вильямса"
        ),
        "trix": TickerIndicator(
            calculator=lambda ticker: ticker.indicator_trix(window=10),
            postfix="%",
            name="Импульсный индикатор"
        ),
        "value": TickerIndicator(
            calculator=lambda ticker: ticker.get_value(),
            postfix=" млн. ₽",
            name="Оборот, млн. ₽"
        )
    }

    # default value is used for lambda-capture
    # for more read: https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
    averages_periods = [5, 10, 20, 50, 100, 200]
    for period in averages_periods:
        Ticker.categories_list["sma" + str(period)] = TickerIndicator(
            calculator=(lambda ticker, window=period: ticker.moving_average(window)),
            postfix="₽",
            name=f"Скользящее среднее за {period} дней"
        )

    for period in averages_periods:
        Ticker.categories_list["ema" + str(period)] = TickerIndicator(
            calculator=(lambda ticker, window=period: ticker.exponential_moving_average(window)),
            postfix="₽",
            name=f"Экспоненциальное скользящее среднее за {period} дней"
        )

    for category in Ticker.categories_list.keys():
        if category.startswith("sma"):
            filename = "sma"
        elif category.startswith("ema"):
            filename = "ema"
        else:
            filename = category

        with open(f"storage/descriptions/{filename}.txt") as file:
            Ticker.categories_list[category].description = "".join(file.readlines())
