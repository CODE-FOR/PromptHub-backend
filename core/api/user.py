from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.models.prompt import Prompt
from core.models.user import User, UserFollowing
from core.models.audit_record import AuditRecord

from .auth import user_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def follow(request: HttpRequest):
    """
    :param request:
        user_id: follow / unfollow user id
    """
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    following_user_id = data.get("user_id")
    if following_user_id is None:
        return failed_parse_data_response()
    
    if not User.objects.filter(id=following_user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "用户不存在")
    following_user = User.objects.get(id=following_user_id)

    user = request.user

    msg = "成功"

    if user.following.filter(id=following_user_id).exists():
        following_relation = UserFollowing.objects.get(user=user, following_user=following_user)
        following_relation.delete()
        msg += "取消关注"
    else:
        UserFollowing.objects.create(user=user, following_user=following_user)
        msg += "关注"

    return success_api_response(
        msg=msg,
        data={
            "following_user_id": following_user_id
        }
    )
    

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_self_published_prompt(request: HttpRequest):

    user = request.user

    """
    :param request:
        page_index: page index, default 1
        per_page: user num per page, default 30
    """
    data = request.GET.dict()

    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)

    paginator = Paginator(Prompt.objects.filter(uploader=user).order_by("-id"), per_page)
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
@user_jwt_auth()
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

    user = request.user

    paginator = Paginator(AuditRecord.objects.filter(status=status, user=user).order_by("-id"), per_page) \
                if status is not None else \
                Paginator(AuditRecord.objects.filter(user=user).order_by("-id"), per_page)
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
@user_jwt_auth()
@require_http_methods("DELETE")
def delete_audit_record(request: HttpRequest):

    user = request.user

    """
    :param request:
        audit_record_id: audit record id
    """
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    audit_record_id = data.get("audit_record_id")
    
    if audit_record_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Prompt.objects.filter(id=audit_record_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "评审记录不存在")
    audit_record = AuditRecord.objects.get(id=audit_record_id)

    if user != audit_record.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限删除该评审记录")
    
    audit_record.delete()

    return success_api_response(
        msg="成功删除该评审记录",
        data = {
            "audit_record_id": audit_record_id
        }
    )