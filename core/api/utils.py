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

def api_responce(code: int, msg: str, data: dict) -> dict:
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

def failed_api_response(status_code, error_msg) -> dict:
    return api_responce(
        code=status_code.value,
        msg=error_msg,
        data={}
    )

def success_api_response(msg: str, data: dict={}) -> dict:
    return api_responce(
        code=StatusCode.SUCCESS.value,
        msg=msg,
        data=data
    )

def response_wrapper(func):
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, dict):
            response = JsonResponse(response)
        return response
    return inner

def failed_parse_data_response():
    return failed_api_response(StatusCode.BAD_REQUEST, "参数解析错误")

def parse_data(request: HttpRequest):
    """POST Request parse data from request.body
    """
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None

def check_data(*args):
    for arg in args:
        if arg is None:
            return False
    return True