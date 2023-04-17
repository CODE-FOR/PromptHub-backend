from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.models.history import History

from .auth import user_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_history_list(request: HttpRequest):
    data = request.GET.dict()
    
    user = request.user
    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))
    histories = user.history_list.all().order_by("-created_at")

    paginator = Paginator(histories, per_page)
    page_history = paginator.page(page_index)

    history_list = []
    for history in page_history.object_list:
        history_list.append(history.simple_dict())

    return success_api_response(
        msg="成功获得历史记录",
        data={
            "history_list": history_list,
            "has_next": page_history.has_next(),
            "has_previous": page_history.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("DELETE")
def delete_history(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user
    history_id = data.get("history_id")
    if history_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not History.objects.filter(id=history_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "历史记录不存在")
    history = History.objects.get(id=history_id)

    if user != history.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限删除该历史记录")
    
    history.delete()

    return success_api_response(msg="成功删除该历史记录")