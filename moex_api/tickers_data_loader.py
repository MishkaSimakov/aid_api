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

            return_value = calculator.get_return()
            dividends_value = calculator.get_dividends()

            if return_value is None or dividends_value is None:
                continue

            result[ticker] = {
                "return": return_value,
                "dividends": dividends_value
            }

        with open("storage/last_data", "w") as storage:
            storage.write(json.dumps(result))

        logging.info("Loaded all tickers.")
    except Exception as e:
        logging.exception(e)

    logging.info("Finished loading tickers.")
