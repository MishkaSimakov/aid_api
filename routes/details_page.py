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

    data = MoexAPI().get_return_for_ticker("SBER")

    return data, 200
