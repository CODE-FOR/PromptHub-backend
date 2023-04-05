from django.http import HttpRequest
from django.views.decorators.http import require_http_methods


from .utils import response_wrapper, parse_data, failed_parse_data_response


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