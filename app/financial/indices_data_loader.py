from app.financial import MoexAPI
from typing import Optional
import logging
from datetime import datetime
import json

from app.config import Paths

required_indices = ['MOEX10', 'MOEXBC', 'MRBC', 'MOEXFN', 'MOEXOG', 'MOEXMM', 'MOEXIT', 'MOEXCN', 'MOEXRE', 'MOEXINN',
                    'MOEXTN', 'MOEXEU', 'MOEXTL', 'MICEXMNF']


def get_names_for_indices(indices: list[str]) -> Optional[dict[str, str]]:
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


def get_tickers_for_index(index: str) -> Optional[dict[str, float]]:
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


def indices_data_loader():
    logging.info("Start reloading indices.")

    try:
        names = get_names_for_indices(required_indices)

        if names is None:
            return

        result = {}

        for index in required_indices:
            tickers = get_tickers_for_index(index)

            result[index] = {
                "name": names[index],
                "tickers": tickers
            }

        with open(Paths.indices_data_path, "w") as storage:
            storage.write(json.dumps({
                "indices": result,
                "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }))

        logging.info("Loaded all indices.")
    except Exception as e:
        logging.exception(e)

    logging.info("Finished loading indices.")
