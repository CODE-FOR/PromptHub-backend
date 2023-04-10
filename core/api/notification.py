from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.models.notification import Notification, UNREAD, SYSTEM_NF, COMMENT_NF

from .auth import user_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

def new_system_notification(passed, prompt_id, content, to_user):
    title = f"作品(id:{prompt_id})审核通过" if passed else f"作品(id:{prompt_id})审核不通过"
    Notification.objects.create(user=to_user, title=title, content=content, status=UNREAD, nf_type=SYSTEM_NF)

def new_comment_notification(username, prompt_id, content, to_user):
    title = f"{username}在你的作品(id:{prompt_id})发表了评论"
    Notification.objects.create(user=to_user, title=title, content=content, status=UNREAD, nf_type=COMMENT_NF)

def new_reply_notification(username, prompt_id, content, to_user):
    title = f"{username}回复了你的评论，作品(id:{prompt_id})"
    Notification.objects.create(user=to_user, title=title, content=content, status=UNREAD, nf_type=COMMENT_NF)

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_notification_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    user = request.user

    nf_type = data.get("nf_type")
    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)
    if nf_type is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    
    notifications = user.notifications.filter(nf_type=nf_type).order_by("-created_at")
    paginator = Paginator(notifications, per_page)
    page_notification = paginator.page(page_index)

    notification_list = []
    for notification in page_notification.object_list:
        notification_list.append(notification.simple_dict())

    return success_api_response(
        msg="成功获得通知",
        data={
            "notification_list": notification_list,
            "has_next": page_notification.has_next(),
            "has_previous": page_notification.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_unread_notification_num(request: HttpRequest):
    user = request.user

    unread_notification = Notification.objects.filter(user=user, status=UNREAD)
    unread_system_notification = unread_notification.filter(nf_type=SYSTEM_NF)
    unread_comment_notification = unread_notification.filter(nf_type=COMMENT_NF)

    return success_api_response(
        msg="获取未读通知数量",
        data={
            "unread_notification_num" : len(unread_notification),
            "unread_system_notification_num": len(unread_system_notification),
            "unread_comment_notification_num": len(unread_comment_notification)
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