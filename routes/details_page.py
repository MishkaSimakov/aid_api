from flask import request
import json

from flask import Blueprint

blueprint = Blueprint('details', __name__)


@blueprint.route("/details", methods=["POST"])
def details():
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        return json.dumps({
            "message": "You've send some cringe."
        }), 400


