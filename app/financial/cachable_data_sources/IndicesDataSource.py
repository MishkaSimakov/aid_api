from app.financial import MoexAPI
from typing import Optional
from app.financial.cachable_data_sources.CachableDataSource import CachableDataSource, DataType


class IndicesDataSource(CachableDataSource):
    __required_indices = ['MOEX10', 'MOEXBC', 'MRBC', 'MOEXFN', 'MOEXOG', 'MOEXMM', 'MOEXIT', 'MOEXCN', 'MOEXRE',
                          'MOEXINN', 'MOEXTN', 'MOEXEU', 'MOEXTL', 'MICEXMNF']

    @staticmethod
    def __get_names_for_indices(indices: list[str]) -> Optional[dict[str, str]]:
        url = f"statistics/engines/stock/markets/index/analytics.json"

        response = MoexAPI().request_with_retry(url)

        if response is None:
            return

        try:
            result = {}
            response_indices = response["indices"]["data"]
            for response_index in response_indices:
                if response_index[0] in indices:
                    result[response_index[0]] = response_index[1]

            return result
        except:
            return

    @staticmethod
    def __get_tickers_for_index(index: str) -> Optional[dict[str, float]]:
        url = f"statistics/engines/stock/markets/index/analytics/{index}.json"

        response = MoexAPI().request_with_retry(url)

        if response is None:
            return

        try:
            result = {}
            tickers_data = response["analytics"]["data"]

            for ticker_data in tickers_data:
                result[ticker_data[2]] = ticker_data[5]

            return result
        except:
            return

    def _load_server_data(self) -> DataType:
        names = self.__get_names_for_indices(self.__required_indices)

        if names is None:
            return

        result = {}

        for index in self.__required_indices:
            tickers = self.__get_tickers_for_index(index)

            result[index] = {
                "name": names[index],
                "tickers": tickers
            }

        return result
