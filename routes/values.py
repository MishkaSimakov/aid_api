from flask import Blueprint
from financial.ticker import Ticker
from utils import with_success

blueprint = Blueprint('values', __name__)


@blueprint.route("/tickers/<ticker>/values", methods=["POST"])
def details(ticker: str):
    ticker = Ticker(name=ticker)

    full_name = ticker.get_full_name()

    values = {}
    for category in Ticker.categories_list.keys():
        values[category] = {
            "value": Ticker.categories_list[category]["calculator"](ticker),
            "postfix": Ticker.categories_list[category]["postfix"],
            "should_buy": False
        }

    return with_success({
        "ticker_full_name": full_name,
        "items": values
    })
