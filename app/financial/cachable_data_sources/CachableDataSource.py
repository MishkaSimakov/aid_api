import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar, Generic, Optional
import uuid
import os

from app import Paths

DataType = TypeVar('DataType')


class CachableDataSource(ABC, Generic[DataType]):
    cache_file_path: os.path

    def __init__(self):
        self.cache_file_path = os.path.join(Paths.cache_data_path, uuid.uuid4().hex)

    @abstractmethod
    def _load_server_data(self) -> DataType:
        pass

    def _has_cached_data(self) -> bool:
        if not os.path.isfile(self.cache_file_path):
            return False

        with open(self.cache_file_path, 'r') as storage:
            try:
                json.loads(storage.readline())
            except:
                return False

        return True

    def _load_cached_data(self) -> Optional[(DataType, datetime)]:
        try:
            with open(self.cache_file_path, 'r') as storage:
                content = json.loads(storage.readline())

                return content["data"], content["updated_at"]
        except:
            return None

    def cache_data(self, data: DataType):
        logging.info(f"Start caching data into file {self.cache_file_path}.")

        try:
            with open(self.cache_file_path, "w") as storage:
                storage.write(json.dumps({
                    "data": data,
                    "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }))
        except Exception as e:
            logging.exception(e)

        logging.info("Finished caching data.")

    def get_data(self) -> DataType:
        if not self._has_cached_data():
            data = self._load_server_data()
            self.cache_data(data)
        else:
            data = self._load_cached_data()

        return data
