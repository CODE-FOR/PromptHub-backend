from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.models.prompt import Prompt, LANCHED
from core.models.user import User, UserFollowing
from core.models.audit_record import AuditRecord

from .auth import user_jwt_auth, get_user_from_token
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

    if user.id == following_user_id:
        return failed_api_response(StatusCode.BAD_REQUEST, "不可以自己关注自己")
        
    msg = "成功"

    if user.following.filter(following_user_id=following_user_id).exists():
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
@require_http_methods("GET")
def get_user_following_num(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    user_id = data.get("user_id", None)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    user = User.objects.get(id=user_id)

    num = len(user.following.all())

    return success_api_response(
        msg="成功获取关注人数",
        data={
            "following_num": num
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_user_following_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    user_id = data.get("user_id", None)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    user = User.objects.get(id=user_id)

    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    paginator = Paginator(user.following.all(), per_page)
    page_following = paginator.page(page_index)

    following_list = []
    for following in page_following.object_list:
        following_list.append(following.following_user.simple_dict())

    return success_api_response(
        msg="成功获取关注列表",
        data={
            "following_list": following_list,
            "has_next": page_following.has_next(),
            "has_previous": page_following.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_user_follower_num(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    user_id = data.get("user_id", None)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    user = User.objects.get(id=user_id)

    num = len(user.followers.all())

    return success_api_response(
        msg="成功获取粉丝人数",
        data={
            "follower_num": num
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_user_follower_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    user_id = data.get("user_id", None)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    user = User.objects.get(id=user_id)

    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    paginator = Paginator(user.followers.all(), per_page)
    page_follower = paginator.page(page_index)

    follower_list = []
    for follower in page_follower.object_list:
        follower_list.append(follower.user.simple_dict())

    return success_api_response(
        msg="成功获取粉丝列表",
        data={
            "follower_list": follower_list,
            "has_next": page_follower.has_next(),
            "has_previous": page_follower.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_published_prompt_num(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    user_id = data.get("user_id", None)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    user = User.objects.get(id=user_id)

    num = len(Prompt.objects.filter(uploader=user, upload_status=LANCHED))

    return success_api_response(
        msg="成功获取作品数量",
        data={
            "prompt_num": num
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_published_prompt_list(request: HttpRequest):
    """
    :param request:
        user_id:
        page_index: page index, default 1
        per_page: user num per page, default 30
    """
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    user_id = data.get("user_id", None)
    if user_id is None or not User.objects.filter(id=user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    user = User.objects.get(id=user_id)

    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    paginator = Paginator(Prompt.objects.filter(uploader=user, upload_status=LANCHED).order_by("-id"), per_page)
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

    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))
    status = int(data.get("status", -1))

    user = request.user

    if status != -1:
        paginator = Paginator(
            AuditRecord.objects.filter(status=status, user=user, user_visible=True, is_delete=False).order_by("-id"), per_page)
    else:
        paginator = Paginator(AuditRecord.objects.filter(user=user, is_delete=False).order_by("-id"), per_page)
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
    
    # audit_record.delete()
    audit_record.be_deleted()

    return success_api_response(
        msg="成功删除该评审记录",
        data = {
            "audit_record_id": audit_record_id
        }
    )

@response_wrapper
@require_http_methods("GET")
def is_following(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, error_msg="参数不完整")
    
    target_user_id = data.get("target_user_id", None)

    user = get_user_from_token(request)
    user_id = -1 if user is None else user.id

    if not User.objects.filter(id=target_user_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="用户不存在")
    
    target_user = User.objects.get(id=target_user_id)

    is_following = False if user_id == -1 \
        else UserFollowing.objects.filter(user=user, following_user=target_user).exists()
    
    return success_api_response(
        msg="获取成功",
        data={
            "is_following": is_following,
            "target_user_id": target_user_id
        }
    )
