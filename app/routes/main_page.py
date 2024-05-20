from flask import request, Blueprint
from app.financial.DataSourcesContainer import DataSourcesContainer
from app.financial.ticker import Ticker
from app.utils import with_error, with_json_fields, with_success

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["POST"])
@with_json_fields(["category"])
def main():
    """
    Путь, по которому можно получить данные для главной страницы сайта.
    Это значение данного параметра для всех доступных тикеров, а также
    распределение тикеров по индексам.
    """

    category_name = request.json["category"]
    if category_name not in Ticker.categories_list:
        return with_error(f"Wrong category type. Available categories: {', '.join(Ticker.categories_list.keys())}")

    tickers_data = DataSourcesContainer.tickers_data_source.get_data()
    indices_data = DataSourcesContainer.indices_data_source.get_data()

    if indices_data is None or tickers_data is None:
        return with_error("Something wrong with internal files.", 500)

    indices_data = indices_data[0]
    tickers_data, updated_at = tickers_data

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
