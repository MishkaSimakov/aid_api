from flask import request
import json

from flask import Blueprint
from moex_api import MoexAPI

blueprint = Blueprint('values', __name__)


@blueprint.route("/tickers/<ticker>/values", methods=["POST"])
def details(ticker: str):
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        return json.dumps({
            "message": "You've send some cringe."
        }), 400



    return "hello", 200
