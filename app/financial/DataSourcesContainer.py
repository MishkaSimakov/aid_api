from app.financial.cachable_data_sources.IndicesDataSource import IndicesDataSource
from app.financial.cachable_data_sources.TickersDataSource import TickersDataSource


class DataSourcesContainer:
    """Хранит в себе объекты классов, загружающие данные с сервера."""

    indices_data_source: IndicesDataSource
    tickers_data_source: TickersDataSource

    @staticmethod
    def init_sources():
        DataSourcesContainer.indices_data_source = IndicesDataSource()
        DataSourcesContainer.tickers_data_source = TickersDataSource()
