import requests


def get_image_url(ticker_name: str) -> str:
    return f"https://finrange.com/storage/companies/logo/svg/MOEX_{ticker_name}.svg"


def get_tickers_list_url() -> str:
    return "https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX/tickers.json"


storage_path = "../storage/images/"
tickers = [x[0] for x in requests.get(get_tickers_list_url()).json()["tickers"]["data"]]

for ticker in tickers:
    response = requests.get(get_image_url(ticker))

    if response.status_code != 200:
        continue

    image_contents = response.content

    with open(storage_path + ticker + ".svg", "+wb") as file:
        file.write(image_contents)
