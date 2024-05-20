from datetime import timedelta
from app.financial import StockDataInterval
from pathlib import Path


class ChartConfig:
    """
    Этот класс содержит доступные периоды для графика цен на тикер.
    В запросе приходит ключ (H, M, ...), а значения delta и interval используются
    для составления запроса к Мосбирже.
    """

    periods = {
        "H": {
            "delta": timedelta(hours=1),
            "interval": StockDataInterval.MINUTE
        },
        "D": {
            "delta": timedelta(days=1),
            "interval": StockDataInterval.TEN_MINUTES
        },
        "W": {
            "delta": timedelta(days=7),
            "interval": StockDataInterval.HOUR
        },
        "M": {
            "delta": timedelta(days=30),
            "interval": StockDataInterval.HOUR
        },
        "Y": {
            "delta": timedelta(days=365),
            "interval": StockDataInterval.WEEK
        },
        "A": {
            "delta": timedelta(days=365 * 100),
            "interval": StockDataInterval.MONTH
        }
    }


class Paths:
    """Здесь заданы пути, которые используются программой."""

    @staticmethod
    def get_storage_path(relative_path: str) -> str:
        """
        Возвращает путь к файлу из папки storage, независимо от того,
        из какой папки запущено приложение.
        """

        return str(Path(__file__).parents[2] / "storage" / relative_path)

    @staticmethod
    def get_client_path(relative_path: str) -> str:
        """
        Возвращает путь к файлу из папки client, независимо от того,
        из какой папки запущено приложение.
        """

        return str(Path(__file__).parents[2] / "client" / relative_path)

    cache_data_path = get_storage_path("cache")
    images_path = get_storage_path("images")
    log_path = get_storage_path("debug.log")
