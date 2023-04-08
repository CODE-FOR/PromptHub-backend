from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.models.user import User
from core.models.prompt import Prompt
from core.models.audit_record import AuditRecord, IN_PROGRESS
from core.models.notification import Notification, UNREAD
from core.models.comment import Comment

from .auth import admin_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_responce, \
                   parse_data, failed_parse_data_response

@response_wrapper
@admin_jwt_auth()
@require_http_methods("GET")
def get_user_list(request: HttpRequest):
    """
    :param request:
        page_index: page index, default 1
        page_size: user num per page, default 30
        sort_by: future feature
    """

    data = request.GET.dict()
    if not data:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")
    
    page_size = data.get("page_size", 30)
    page_index = data.get("page_index", 1)

    # TODO: sort user
    paginator = Paginator(User.objects.all(), page_size)
    page_user = paginator.page(page_index)

    user_list = []
    for user in page_user.object_list:
        user_list.append(user.manage_dict())

    return success_api_response(
        msg="成功获取用户列表",
        data={
            "user_list": user_list,
            "has_next": page_user.has_next(),
            "has_previous": page_user.has_previous(),
            "page_num": paginator.num_pages
        }
    )


@response_wrapper
@admin_jwt_auth()
@require_http_methods("GET")
def get_prompt_list(request: HttpRequest):
    """
    :param request:
        page_index: page index, default 1
        per_page: user num per page, default 30
        sort_by: future feature
    """

    data = request.GET.dict()
    if not data:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")

    page_size = data.get("page_size", 30)
    page_index = data.get("page_index", 1)

    # TODO: sort prompt
    paginator = Paginator(Prompt.objects.all(), page_size)
    page_prompt = paginator.page(page_index)

    prompt_list = []
    for prompt in page_prompt.object_list:
        prompt_list.append(prompt.simple_dict())
    
    return success_api_response(
        msg="成功获取Prompt",
        data={
            "prompt_list": prompt_list,
            "has_next": page_prompt.has_next(),
            "has_previous": page_prompt.has_previous(),
            "page_num": paginator.num_pages
        }
    )


@response_wrapper
@admin_jwt_auth()
@require_http_methods("GET")
def get_audit_record_list(request: HttpRequest):
    """
    :param request:
        page_index: page index, default 1
        per_page: user num per page, default 30
        sort_by: future feature
    """

    data = request.GET.dict()

    page_size = data.get("page_size", 30)
    page_index = data.get("page_index", 1)

    # TODO: sort prompt
    paginator = Paginator(AuditRecord.objects.filter(status=IN_PROGRESS), page_size)
    page_audit_record = paginator.page(page_index)

    audit_record_list = []
    for audit_record in page_audit_record.object_list:
        audit_record_list.append(audit_record.review_list_dict())
    
    return success_api_response(
        msg="成功获取待审核Prompt",
        data={
            "prompt_list": audit_record_list,
            "has_next": page_audit_record.has_next(),
            "has_previous": page_audit_record.has_previous(),
            "page_num": paginator.num_pages
        }
    )


@response_wrapper
@admin_jwt_auth()
@require_http_methods("POST")
def pass_prompt(request: HttpRequest):
    """
    :param request:
        id: audit record id
    """

    data = parse_data(request)
    if not data:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")
    
    id = data.get("id")
    if id is None:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")

    audit_record = AuditRecord.objects.get(id=id)
    prompt = audit_record.prompt

    prompt.be_lanched()
    audit_record.be_passed()

    '''notify the uploader about upload status'''
    uploader = audit_record.user
    Notification.objects.create(
        user=uploader,
        # TODO: change this msg
        content=f"您的作品{prompt.id}审核通过",
        status = UNREAD
    )

    return success_api_response(
        msg="审核通过",
        data={
            "id": id,
            "uploader_id": uploader.id
        }
    )

@response_wrapper
@admin_jwt_auth()
@require_http_methods("POST")
def take_down_prompt(request: HttpRequest):
    """
    :param request:
        id: audit record id
        reject_reason: reject reason
    """

    data = parse_data(request)
    if not data:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")
    
    id = data.get("id")
    reject_reason = data.get("reject_reason", None)
    if id is None:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")

    audit_record = AuditRecord.objects.get(id=id)
    prompt = audit_record.prompt

    audit_record.be_rejected()

    '''notify the uploader about upload status'''
    uploader = prompt.uploader
    Notification.objects.create(
        user=uploader,
        content=f"您的作品{id}由于{reject_reason}审核不通过，请修改后重新上传",
        status = UNREAD
    )

    return success_api_response(
        msg="审核不通过",
        data={
            "id": id,
            "uploader_id": uploader.id
        }
    )


@response_wrapper
@admin_jwt_auth()
@require_http_methods("GET")
def get_comment_list(request: HttpRequest):
    """
    :param request:
        prompt_id: comments' prompt id
        page_size: comments num per page
        page_index: page index
    """
    data = request.GET.dict()
    if not data:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")
    
    prompt_id = data.get("prompt_id")
    page_size = data.get("page_size", 30)
    page_index = data.get("page_index", 1)
    if prompt_id is None:
        return failed_api_responce(StatusCode.BAD_REQUEST, "参数错误")
    
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_responce(StatusCode.BAD_REQUEST, "作品不存在")
    
    prompt = Prompt.objects.get(id=prompt_id)

    paginator = Paginator(prompt.comment_list.all(), page_size)
    page_comments = paginator.page(page_index)

    comment_list = []
    for comment in page_comments.object_list:
        comment_list.append(comment.full_dict())

    return success_api_response(
        msg="成功获得评论列表",
        data={
            "comment_list": comment_list,
            "page_size": paginator.num_pages
        }
    )

@response_wrapper
@admin_jwt_auth()
@require_http_methods("DELETE")
def delete_comment(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    comment_id = data.get("comment_id")
    if not Comment.objects.filter(id=comment_id).exists():
        return failed_api_responce(StatusCode.ID_NOT_EXISTS, "评论不存在")
    comment = Comment.objects.get(id=comment_id)
     
    comment.delete()
    return success_api_response(msg="成功删除评论")
