import requests
from cairosvg import svg2png

"""
Этот скрипт загружает изображения для тикеров с сайта с финансами и сохраняет их в локальную папку.
"""


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

    svg2png(bytestring=image_contents, write_to=storage_path + ticker + ".png", output_width=512, output_height=512)
