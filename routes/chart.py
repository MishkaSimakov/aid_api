from typing import Dict

from flask import request
import json
from utils import with_error, with_json_fields, with_success
from config.categories import ChartConfig
from datetime import datetime

from flask import Blueprint
from financial import MoexAPI, Candle

blueprint = Blueprint('chart', __name__)


def format_candle(candle: Candle) -> Dict[str, str]:
    return {
        "value": candle.open,
        "begin": candle.begin.strftime('%Y-%m-%d %H:%M:%S'),
        "end": candle.end.strftime('%Y-%m-%d %H:%M:%S'),
    }


@blueprint.route("/tickers/<ticker>/chart", methods=["POST"])
@with_json_fields(["period"])
def chart(ticker: str):
    period = request.json["period"]

    if period not in ChartConfig.periods:
        return with_error(f"Period is not supported. Supported periods are: {', '.join(ChartConfig.periods.keys())}.")

    end_date = datetime.now()
    start_date = end_date - ChartConfig.periods[period]["delta"]
    interval = ChartConfig.periods[period]["interval"]
    data = MoexAPI().get_candles(ticker, start_date, end_date, interval, count=30)

    return with_success({
        "items": list(map(format_candle, data))
    })
