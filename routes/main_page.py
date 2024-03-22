import logging

from flask import request
import json
from flask import Blueprint
from financial.ticker import Ticker

from config.categories import CategoriesConfig
from utils import with_error, with_json_fields, with_success

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["POST"])
@with_json_fields(["category"])
def main():
    category_name = request.json["category"]
    if category_name not in Ticker.categories_list:
        return with_error(f"Wrong category type. Available categories: {', '.join(Ticker.categories_list.keys())}")

    try:
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
        "postfix": category["postfix"]
    })
