from app.financial import MoexAPI
import json
import logging
from datetime import datetime

from app.financial.ticker import Ticker
from app.config import Paths


def tickers_data_loader():
    logging.info("Start reloading tickers.")

    try:
        tickers_names = MoexAPI().get_tickers()
        tickers = [Ticker(name) for name in tickers_names]
        tickers_data = {}

        for ticker in tickers:
            tickers_data[ticker.name] = {}

            for category_name in Ticker.categories_list.keys():
                result = Ticker.categories_list[category_name].calculator(ticker)

                tickers_data[ticker.name][category_name] = result.value if result is not None else None

        with open(Paths.tickers_data_path, "w") as storage:
            storage.write(json.dumps({
                "tickers": tickers_data,
                "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }))

        logging.info("Loaded all tickers.")
    except Exception as e:
        logging.exception(e)

    logging.info("Finished loading tickers.")
