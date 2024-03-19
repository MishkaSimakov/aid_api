from flask import request
import json

from flask import Blueprint

blueprint = Blueprint('main', __name__)

@blueprint.route("/", methods=["POST"])
def main():
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        return json.dumps({
            "message": "You've send some cringe."
        }), 400

    return json.dumps({
        "message": "Success!",
        "items": {
            "SBER": 0.029,
            "ROSN": 0.033,
            "VTB": -0.010,
            "TCSG": 0.046,
            "OZON": -0.01,
            "FIVE": 0.021,
            "SFIN": 0.017,
            "PLZL": -0.006,
            "CRTX": 0.000,
            "STZ": -0.005,
            "UBER": 0.012
        },
        "postfix": "%"
    }), 200