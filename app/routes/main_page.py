import logging
from flask import request, Blueprint
import json

from app import Paths
from app.financial.ticker import Ticker
from app.utils import with_error, with_json_fields, with_success

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["POST"])
@with_json_fields(["category"])
def main():
    category_name = request.json["category"]
    if category_name not in Ticker.categories_list:
        return with_error(f"Wrong category type. Available categories: {', '.join(Ticker.categories_list.keys())}")

    try:
        with open(Paths.tickers_data_path) as storage:
            data = json.loads(storage.readline())
            tickers_data = data["tickers"]
            updated_at = data["updated_at"]
    except Exception as e:
        logging.exception(e)
        return with_error("Something wrong with internal files.", 500)


    indices_data = json.loads(storage.readline())["indices"]
    return with_error("Something wrong with internal files.", 500)

    category = Ticker.categories_list[category_name]

    result = {}
    for ticker in tickers_data:
        result[ticker] = {
            "value": tickers_data[ticker][category_name],
        }

    return with_success({
        "tickers": result,
        "indices": indices_data,
        "updated_at": updated_at,
        "postfix": category.postfix
    })
