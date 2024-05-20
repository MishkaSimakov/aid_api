import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, Generic, Optional, Tuple
import os

DataType = TypeVar('DataType')


class CachableDataSource(ABC, Generic[DataType]):
    """
    Этот абстрактный класс управляет данными, загружаемыми с сервера.
    Он поддерживает кэширование данных в файл для более быстрого доступа.
    """

    @staticmethod
    @abstractmethod
    def _get_cache_filepath() -> os.path:
        """
        Перегружается в реализациях, возвращает путь к файлу,
        в котором будут храниться данные
        """
        pass

    @abstractmethod
    def _load_server_data(self) -> DataType:
        """
        Перегружается в реализациях, возвращает загруженные с сервера данные.
        """
        pass

    def _has_cached_data(self) -> bool:
        """
        Проверяет, есть ли доступные данные в файле.
        При этом проверяется лишь наличие данных, не их корректность.
        """

        if not os.path.isfile(self._get_cache_filepath()):
            return False

        with open(self._get_cache_filepath(), 'r') as storage:
            try:
                json.loads(storage.readline())
            except:
                return False

        return True

    def _load_cached_data(self) -> Optional[Tuple[DataType, datetime]]:
        """Загружает закэшированные данные из файла."""

        try:
            with open(self._get_cache_filepath(), 'r') as storage:
                content = json.loads(storage.readline())

                return content["data"], content["updated_at"]
        except:
            return None

    def cache_data(self, data: DataType):
        """Кэширует данные, загружая их в файл."""

        logging.info(f"Start caching data into file {self._get_cache_filepath()}.")

        try:
            with open(self._get_cache_filepath(), "w+") as storage:
                storage.write(json.dumps({
                    "data": data,
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }))
        except Exception as e:
            logging.exception(e)

        logging.info("Finished caching data.")

    def load_from_server_and_cache(self):
        """Загружает данные с сервера и записывает их в файл."""

        data = self._load_server_data()
        self.cache_data(data)

    def get_data(self) -> Optional[Tuple[DataType, datetime]]:
        """
        Возвращает загруженные данные.
        Если в файле с кэшем что-то есть - возвращает эти данные,
        а иначе загружает данные с сервера и кэширует их.
        """

        if not self._has_cached_data():
            self.load_from_server_and_cache()

        return self._load_cached_data()
