from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.models.notification import Notification

from .auth import user_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_notification_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    user = request.user

    nf_type = data.get("nf_type")
    page_size = data.get("page_size", 30)
    page_index = data.get("page_index", 1)
    if nf_type is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    
    notifications = user.notifications.filter(nf_type=nf_type).order_by("-created_at")
    paginator = Paginator(notifications, page_size)
    page_notification = paginator.page(page_index)

    notification_list = []
    for notification in page_notification.object_list:
        notification_list.append(notification.simple_dict())

    return success_api_response(
        msg="成功获得通知",
        data={
            "notification_list": notification_list
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def update_notification(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    user = request.user
    notification_id = data.get("id")
    status = data.get("status")

    if not Notification.objects.filter(id=notification_id).exists():
        return failed_api_response(StatusCode.BAD_REQUEST, "通知不存在")
    notification = Notification.objects.get(id=notification_id)

    if user != notification.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限修改该历史记录状态")
    
    notification.status = status
    notification.save()

    return success_api_response(msg="成功更新通知状态")

@response_wrapper
@user_jwt_auth()
@require_http_methods("DELETE")
def delete_notification(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user
    notification_id = data.get("id")
    if notification_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Notification.objects.filter(id=notification_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "通知不存在")
    notification = Notification.objects.get(id=notification_id)

    if user != notification.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限删除该通知")
    
    notification.delete()

    return success_api_response(msg="成功删除该通知")