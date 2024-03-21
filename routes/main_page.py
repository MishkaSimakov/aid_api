from flask import request
import json
from flask import Blueprint

from config.categories import CategoriesConfig
from utils import with_error

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["POST"])
def main():
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/json':
        return with_error("Wrong content type")

    data = request.json
    if "category" not in data:
        return with_error("There must be category field")
    if data["category"] not in CategoriesConfig.categories:
        return with_error("Wrong category type")

    with open("storage/last_data") as storage:
        values = json.loads(storage.readline())

    category = CategoriesConfig.categories[data["category"]]

    result = {}
    for company in values:
        result[company] = {
            "value": values[company]["return"] * 100
        }

    return json.dumps({
        "message": "success",
        "items": result,
        "postfix": category.postfix
    }), 200
