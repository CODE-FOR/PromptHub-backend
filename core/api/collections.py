from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from core.models.user import User, ConfirmCode

from .auth import user_jwt_auth
from .send_email import send_sign_in_email, send_forget_password_email
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_responce, \
                   parse_data, failed_parse_data_response


@response_wrapper
@require_http_methods("POST")
def add_to_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()


@response_wrapper
@require_http_methods("POST")
def del_from_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()


@response_wrapper
@require_http_methods("POST")
def mod_collection_attribute(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

@response_wrapper
@require_http_methods("POST")
def create_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

@response_wrapper
@require_http_methods("POST")
def delete_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

@response_wrapper
@require_http_methods("POST")
def mod_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()