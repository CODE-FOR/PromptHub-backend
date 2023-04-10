from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.api.notification import new_system_notification

from core.models.user import User
from core.models.prompt import Prompt
from core.models.audit_record import AuditRecord
from core.models.comment import Comment

from .auth import admin_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

@response_wrapper
@admin_jwt_auth()
@require_http_methods("GET")
def get_user_list(request: HttpRequest):
    """
    :param request:
        page_index: page index, default 1
        per_page: user num per page, default 30
    """

    data = request.GET.dict()
    
    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)

    paginator = Paginator(User.objects.all().order_by("id"), per_page)
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
            "page_index": page_index,
            "page_total": paginator.num_pages
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
    """
    data = request.GET.dict()

    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)

    paginator = Paginator(Prompt.objects.all().order_by("-id"), per_page)
    page_prompt = paginator.page(page_index)

    prompt_list = []
    for prompt in page_prompt.object_list:
        prompt_list.append(prompt.full_dict())
    
    return success_api_response(
        msg="成功获取Prompt",
        data={
            "prompt_list": prompt_list,
            "has_next": page_prompt.has_next(),
            "has_previous": page_prompt.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
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
        status: 
    """

    data = request.GET.dict()

    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)
    status = data.get("status", None)

    paginator = Paginator(AuditRecord.objects.filter(status=status).order_by("-id"), per_page) \
                if status is not None else \
                Paginator(AuditRecord.objects.all().order_by("-id"), per_page)
    page_audit_record = paginator.page(page_index)

    audit_record_list = []
    for audit_record in page_audit_record.object_list:
        audit_record_list.append(audit_record.to_dict())
    
    return success_api_response(
        msg="成功获取Prompt审核记录",
        data={
            "audit_record_list": audit_record_list,
            "has_next": page_audit_record.has_next(),
            "has_previous": page_audit_record.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )


@response_wrapper
@admin_jwt_auth()
@require_http_methods("POST")
def audit_prompt(request: HttpRequest):
    """
    :param request:
        id: audit record id
        passed: bool
        content: content
    """
    data = parse_data(request)
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    id = data.get("id")
    passed = data.get("passed")
    content = data.get("content", "")
    if id is None or passed is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")

    audit_record = AuditRecord.objects.get(id=id)
    audit_record.feedback = content
    audit_record.save()
    prompt = audit_record.prompt

    if passed:
        prompt.be_lanched()
        audit_record.be_passed()
    else:
        audit_record.be_rejected()

    '''notify the uploader about upload status'''
    uploader = audit_record.user
    new_system_notification(passed=passed, prompt_id=prompt.id, content=content, to_user=uploader)

    return success_api_response(
        msg="完成审核",
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
        per_page: comments num per page
        page_index: page index
    """
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    prompt_id = data.get("prompt_id")
    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.BAD_REQUEST, "作品不存在")
    
    prompt = Prompt.objects.get(id=prompt_id)

    paginator = Paginator(prompt.comment_list.all().order_by("created_at"), per_page)
    page_comments = paginator.page(page_index)

    comment_list = []
    for comment in page_comments.object_list:
        comment_list.append(comment.full_dict())

    return success_api_response(
        msg="成功获得评论列表",
        data={
            "comment_list": comment_list,
            "has_next": page_comments.has_next(),
            "has_previous": page_comments.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
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
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "评论不存在")
    comment = Comment.objects.get(id=comment_id)
     
    comment.delete()
    return success_api_response(msg="成功删除评论")