import json
from functools import wraps
from flask import request


def with_error(error: str, code: int = 400) -> (str, int):
    return json.dumps({
        "message": error
    }), code


def with_json_fields(fields: list[str]):
    def decorator(callback):
        @wraps(callback)
        def callback_wrapper(*args, **kwargs):
            content_type = request.headers.get('Content-Type')

            if content_type != 'application/json':
                return with_error("Content type must be application/json")

            try:
                content = request.json
            except:
                return with_error("JSON is illegible.")

            for field in fields:
                if field not in content:
                    return with_error(f"Request must contain {field} field.")

            return callback(*args, **kwargs)

        return callback_wrapper

    return decorator
