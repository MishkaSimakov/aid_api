from typing import Dict

from flask import request
import json
from utils import with_error
from config.categories import ChartConfig
from datetime import datetime

from flask import Blueprint
from moex_api import MoexAPI, Candle

blueprint = Blueprint('chart', __name__)


def format_candle(candle: Candle) -> Dict[str, str]:
    return {
        "value": candle.open,
        "begin": candle.begin.strftime('%Y-%m-%d %H:%M:%S'),
        "end": candle.end.strftime('%Y-%m-%d %H:%M:%S'),
    }


@blueprint.route("/tickers/<ticker>/chart", methods=["POST"])
def chart(ticker: str):
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        return with_error("You've send some cringe.")

    if "period" not in request.json:
        return with_error("Period must be specified.")

    period = request.json["period"]

    if period not in ChartConfig.periods:
        return with_error("Interval is not supported.")

    end_date = datetime.now()
    start_date = end_date - ChartConfig.periods[period]["delta"]
    interval = ChartConfig.periods[period]["interval"]
    data = MoexAPI().get_candles(ticker, start_date, end_date, interval, count=30)

    return json.dumps({
        "message": "success",
        "items": list(map(format_candle, data))
    }), 200
