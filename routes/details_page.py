from flask import request
import json

from flask import Blueprint
from moex_api import MoexAPI

blueprint = Blueprint('details', __name__)


@blueprint.route("/details", methods=["POST"])
def details():
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        return json.dumps({
            "message": "You've send some cringe."
        }), 400

    tickers = MoexAPI().get_tickers()
    for ticker in tickers:
        print(ticker)
        print(MoexAPI().get_last_data_for_ticker(ticker))

    return "hello", 200
