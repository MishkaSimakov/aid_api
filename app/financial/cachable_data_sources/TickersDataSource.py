from app.financial.ticker import Ticker
import os
from app import Paths
from app.financial import MoexAPI
from app.financial.cachable_data_sources.CachableDataSource import CachableDataSource, DataType


class TickersDataSource(CachableDataSource):
    """Загружает данные о тикерах с api Мосбиржи."""

    @staticmethod
    def _get_cache_filepath() -> os.path:
        return os.path.join(Paths.cache_data_path, 'tickers')

    def _load_server_data(self) -> DataType:
        tickers_names = MoexAPI().get_tickers()
        tickers = [Ticker(name, 'ru') for name in tickers_names]
        tickers_data = {}

        for ticker in tickers:
            tickers_data[ticker.name] = {}

            for category_name in Ticker.categories_list.keys():
                result = Ticker.categories_list[category_name].calculator(ticker)

                tickers_data[ticker.name][category_name] = result.value if result is not None else None

        return tickers_data
