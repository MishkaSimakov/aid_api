from moex_api import MoexAPI
import json
from time import sleep
from datetime import datetime, timedelta

from moex_api import StockDataInterval


def tickers_data_loader():
    print("Loading last tickers data...")
    # try:
    tickers = MoexAPI().get_tickers()
    result = {}

    prev_day: datetime = datetime.today() - timedelta(days=1)
    prev_day_start: str = f"{prev_day.strftime('%Y-%m-%d')} 09:00:00"
    prev_day_end: str = f"{prev_day.strftime('%Y-%m-%d')} 23:00:00"

    for ticker in tickers:
        ticker_data = MoexAPI().get_last_data_for_ticker(ticker)

        if len(ticker_data) == 0:
            continue

        prev_day_start_row = ticker_data[0]
        prev_day_end_row = ticker_data[-1]

        result[ticker] = {
            "return": (prev_day_end_row[1] - prev_day_start_row[0]) / prev_day_start_row[0]
        }

    with open("storage/last_data", "w") as storage:
        storage.write(json.dumps(result))

    print("Loaded all tickers")
    # except:
    #     print("Loading failed, will try again next time")
