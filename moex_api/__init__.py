import apimoex
import requests


class MoexAPI:
    def get_tickers_list(self):
        index_id = 'IMOEX'

        with requests.Session() as session:
            data = apimoex.get_index_tickers(session, index_id)

        return [x["ticker"] for x in data]

    def get_return_for_ticker(self, ticker: str):
        with requests.Session() as session:
            data = apimoex.get_market_candles(session, ticker, 1)

        return data