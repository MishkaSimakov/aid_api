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

        curr_day = ticker_data[-1]
        prev_day = ticker_data[0]

        result[ticker] = {
            "return": (curr_day.close / prev_day.close - 1) * 100
        }

    with open("storage/last_data", "w") as storage:
        storage.write(json.dumps(result))

    print("Loaded all tickers")
    # except:
    #     print("Loading failed, will try again next time")
