from flask import Blueprint
from app.financial.ticker import Ticker
from app.utils import with_success

blueprint = Blueprint('values', __name__)


@blueprint.route("/tickers/<ticker>/values", methods=["GET"])
def details(ticker: str):
    ticker = Ticker(name=ticker)

    short_name, full_name = ticker.get_names()

    values = {}
    for category_name in Ticker.categories_list.keys():
        category = Ticker.categories_list[category_name]
        values[category_name] = category.calculate_for_ticker(ticker)

    return with_success({
        "short_name": short_name,
        "full_name": full_name,
        "items": values
    })
