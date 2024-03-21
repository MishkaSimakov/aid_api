from moex_api import MoexAPI
import json


def tickers_data_loader():
    print("Loading last tickers data...")
    # try:
    tickers = MoexAPI().get_tickers()
    result = {}

    for ticker in tickers:
        ticker_data = MoexAPI().get_last_day_candles(ticker)

        if len(ticker_data) == 0:
            continue

        prev_day_start_row = ticker_data[0]
        prev_day_end_row = ticker_data[-1]

        result[ticker] = {
            "return": (prev_day_end_row.close - prev_day_start_row.open) / prev_day_start_row.open
        }

    with open("storage/last_data", "w") as storage:
        storage.write(json.dumps(result))

    print("Loaded all tickers")
    # except:
    #     print("Loading failed, will try again next time")
