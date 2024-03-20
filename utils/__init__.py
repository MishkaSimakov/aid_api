import json


def with_error(error: str, code: int = 400) -> (str, int):
    return json.dumps({
        "message": error
    }), code
