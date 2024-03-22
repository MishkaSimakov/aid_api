from flask import Blueprint
from app.financial.ticker import Ticker
from app.utils import with_success

blueprint = Blueprint('values', __name__)


@blueprint.route("/tickers/<ticker>/values", methods=["POST"])
def details(ticker: str):
    ticker = Ticker(name=ticker)

    full_name = ticker.get_full_name()

    values = {}
    for category_name in Ticker.categories_list.keys():
        category = Ticker.categories_list[category_name]
        values[category_name] = {
            "value": category["calculator"](ticker),
            "postfix": category["postfix"],
            "description": category["description"],
            "should_buy": False
        }

    return with_success({
        "ticker_full_name": full_name,
        "items": values
    })
