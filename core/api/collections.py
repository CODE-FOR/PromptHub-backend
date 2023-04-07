from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from .utils import response_wrapper, parse_data, failed_parse_data_response, check_data, failed_api_response, \
    StatusCode, success_api_response
from .auth import user_jwt_auth
from core.models.collection import Collection, CollectRecord


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def add_to_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def remove_from_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()


'''
create a new collection
'''


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def create_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    user = request.user
    name = data.get("name")
    visibility = data.get("visibility")

    if not check_data(name, visibility):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if len(name) > 50:
        return failed_api_response(StatusCode.BAD_REQUEST, "名字过长")

    if Collection.objects.filter(name=name).exists():
        return failed_api_response(StatusCode.CONFLICT, "不可以使用重复的名字")

    Collection.objects.create(name=name, user=user, visibility=visibility)
    return success_api_response(msg="成功")


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def delete_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def mod_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
