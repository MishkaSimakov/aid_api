from flask import request
import json

from flask import Blueprint
from moex_api import MoexAPI

blueprint = Blueprint('values', __name__)


@blueprint.route("/tickers/<ticker>/values", methods=["POST"])
def details(ticker: str):
        

    return "hello", 200
