from moex_api import MoexAPI
import json
import logging
from finance_calculations import FinancialCalculator


def tickers_data_loader():
    logging.info("Start reloading tickers.")

    try:
        tickers = MoexAPI().get_tickers()
        result = {}

        for ticker in tickers:
            calculator = FinancialCalculator(ticker)

            result[ticker] = {
                "return": calculator.get_return(),
                "dividends": calculator.get_dividends()
            }

        with open("storage/last_data", "w") as storage:
            storage.write(json.dumps(result))

        logging.info("Loaded all tickers.")
    except Exception as e:
        logging.exception(e)

    logging.info("Finished loading tickers.")
