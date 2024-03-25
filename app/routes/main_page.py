import logging
import os

from flask import request
import json
from flask import Blueprint
from app.financial.ticker import Ticker

from app.utils import with_error, with_json_fields, with_success
from app.financial.tickers_data_loader import tickers_data_loader

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["GET"])
@with_json_fields(["category"])
def main():
    category_name = request.json["category"]
    if category_name not in Ticker.categories_list:
        return with_error(f"Wrong category type. Available categories: {', '.join(Ticker.categories_list.keys())}")

    try:
        if not os.path.isfile("storage/last_data"):
            tickers_data_loader()

        with open("storage/last_data") as storage:
            values = json.loads(storage.readline())
    except Exception as e:
        logging.exception(e)
        return with_error("Something wrong with internal files.", 500)

    category = Ticker.categories_list[category_name]

    result = {}
    tickers_data = values["tickers"]
    for ticker in tickers_data:
        result[ticker] = {
            "value": values["tickers"][ticker][category_name]
        }

    return with_success({
        "items": result,
        "updated_at": values["updated_at"],
        "postfix": category.postfix
    })
