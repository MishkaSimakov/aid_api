from flask import request
import json
from flask import Blueprint

from config.categories import CategoriesConfig
from utils import with_error, with_json_fields

blueprint = Blueprint('main', __name__)


@blueprint.route("/", methods=["POST"])
@with_json_fields(["category"])
def main():
    category_name = request.json["category"]
    if category_name not in CategoriesConfig.categories:
        return with_error("Wrong category type")

    with open("storage/last_data") as storage:
        values = json.loads(storage.readline())

    category = CategoriesConfig.categories[category_name]

    result = {}
    for company in values:
        result[company] = {
            "value": values[company][category_name] * 100
        }

    return json.dumps({
        "message": "success",
        "items": result,
        "postfix": category["postfix"]
    }), 200
