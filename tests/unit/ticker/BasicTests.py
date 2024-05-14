import unittest
from unittest.mock import MagicMock
from app.financial.ticker import Ticker


class TickerBasicTests(unittest.TestCase):
    fakeTicker: Ticker

    def setUp(self):
        self.fakeTicker = Ticker("YNDX")

        self.fakeTicker.moex_api.get_candles = MagicMock()
        self.fakeTicker.moex_api.get_ticker_info = MagicMock()
        self.fakeTicker.moex_api.get_dividends = MagicMock()

    def test_it_use_moex_api_to_load_data(self):
        self.fakeTicker.load_daily_candles()
        self.fakeTicker.moex_api.get_candles.assert_called_once()

        self.fakeTicker.get_names()
        self.fakeTicker.moex_api.get_ticker_info.assert_called_once_with("YNDX")

        self.fakeTicker.get_dividends()
        self.fakeTicker.moex_api.get_dividends.assert_called_once()

    def test_it_load_data_from_server_only_once(self):
        self.fakeTicker.get_current_price()
        self.fakeTicker.get_current_price()

        self.fakeTicker.moex_api.get_candles.assert_called_once()
