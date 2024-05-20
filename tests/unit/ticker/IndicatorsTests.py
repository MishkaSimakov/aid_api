import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from app.financial import Candle, TickerDividends
from app.financial.ticker import Ticker


class TickerIndicatorsTests(unittest.TestCase):
    """
    Тестируются только те индикаторы, вычисление которых реализовано в самом классе Ticker.
    Мы полагаемся на тестировщиков библиотек pandas и technical_analysis
    """

    fakeTicker: Ticker

    def setUp(self):
        self.fakeTicker = Ticker("YNDX")

        fake_candles = []

        open_time = datetime.now().replace(hour=9, minute=0, second=0)
        close_time = datetime.now().replace(hour=23, minute=0, second=0)

        for day in range(365):
            candle = Candle(
                open=day + 1,
                close=day + 2,
                high=day * 2,
                low=day / 2,
                value=1,
                volume=5,
                begin=open_time - timedelta(days=364 - day),
                end=close_time - timedelta(days=364 - day)
            )

            fake_candles.append(candle)

        fake_dividends = [
            TickerDividends(value=100, close_date=datetime.now() - timedelta(days=1)),
            TickerDividends(value=1000, close_date=datetime.now() - timedelta(days=100))
        ]

        self.fakeTicker.moex_api.get_candles = MagicMock(return_value=fake_candles)
        self.fakeTicker.moex_api.get_ticker_info = MagicMock()
        self.fakeTicker.moex_api.get_dividends = MagicMock(return_value=fake_dividends)

    def test_profitability(self):
        indicator_result = self.fakeTicker.get_profitability()

        self.assertAlmostEqual((366 / 365 - 1) * 100, indicator_result.value)
        self.assertEqual(indicator_result.verdict, 0)

    def test_dividends(self):
        indicator_result = self.fakeTicker.get_dividends()

        self.assertEqual(1100, indicator_result.value)
        self.assertEqual(0, indicator_result.verdict)

    def test_relative_dividends(self):
        indicator_result = self.fakeTicker.get_relative_dividends()
        start_ticker_cost = 1

        self.assertAlmostEqual(1100 / start_ticker_cost * 100, indicator_result.value)
        self.assertEqual(0, indicator_result.verdict)

    def test_value(self):
        indicator_result = self.fakeTicker.get_value()

        self.assertAlmostEqual(1 / 1e6, indicator_result.value)
        self.assertEqual(None, indicator_result.verdict)
