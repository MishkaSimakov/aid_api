from app.utils import *
from flask import Blueprint
from app.financial.ticker import Ticker

blueprint = Blueprint('categories', __name__)


@blueprint.route("/categories", methods=["POST"])
def categories():
    """Этот путь возвращает список доступных индикаторов для тикеров."""

    return with_success({
        "categories": list(Ticker.categories_list.keys())
    })
