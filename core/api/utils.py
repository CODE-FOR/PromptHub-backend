"""
utils for generating api responses
"""
import json
from enum import Enum, unique

from django.http import JsonResponse, HttpRequest

@unique
class StatusCode(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    SERVER_ERROR = 501
    ID_NOT_EXISTS = 555

def api_responce(code: int, data: dict) -> dict:
    return {
        "code": code,
        "data": data
    }

def failed_api_responce(status_code, error_msg=None) -> dict:
    if error_msg is None:
        error_msg = str(status_code)
    else:
        error_msg = str(status_code) + ': ' + error_msg

    return api_responce(
        code=status_code.value,
        data={
            "error_msg": error_msg
        }
    )

def success_api_response(data: dict) -> dict:
    return api_responce(
        code=StatusCode.SUCCESS.value,
        data=data
    )

def response_wrapper(func):
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, dict):
            response = JsonResponse(response["data"])
        return response
    return inner

def failed_parse_data_response():
    return failed_api_responce(StatusCode.BAD_REQUEST, "Parse Data Error")

def parse_data(request: HttpRequest):
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None