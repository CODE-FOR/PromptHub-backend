from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from core.api.notification import new_comment_notification, new_reply_notification

from core.models.comment import Comment
from core.models.prompt import Prompt

from .auth import user_jwt_auth, get_user_from_token
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def create_comment(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user
    
    prompt_id = data.get("prompt_id")
    content = data.get("content")
    parent_comment_id = data.get("parent_comment_id", None)

    if prompt_id is None or content is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if len(content) > 4096:
        return failed_api_response(StatusCode.BAD_REQUEST, "回复内容过长, 请控制在4096字符内")

    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt = Prompt.objects.get(id=prompt_id)

    parent_comment = None
    if parent_comment_id is not None:
        if not Comment.objects.filter(id=parent_comment_id).exists():
            return failed_api_response(StatusCode.ID_NOT_EXISTS, "回复的评论不存在")
        parent_comment = Comment.objects.get(id=parent_comment_id)
        to_user = parent_comment.user
        if to_user != user:
            new_reply_notification(username=user.nickname, prompt=prompt,
                                   content=content, to_user=parent_comment.user)
    else:
        if user != prompt.uploader:
            new_comment_notification(username=user.nickname, prompt=prompt,
                                     content=content, to_user=prompt.uploader)

    comment = Comment.objects.create(prompt=prompt, user=user, content=content, parent_comment=parent_comment)
    return success_api_response(
        msg="成功评论",
        data={
            "id": comment.id
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("DELETE")
def delete_comment(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user

    comment_id = data.get("comment_id")
    if not Comment.objects.filter(id=comment_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "评论不存在")
    comment = Comment.objects.get(id=comment_id)

    if user.id != comment.user.id:
        return failed_api_response(StatusCode.BAD_REQUEST, "该用户无权限删除此评论")
    comment.delete()
    return success_api_response(msg="成功删除评论")

@response_wrapper
@require_http_methods("GET")
def get_comment_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    user = get_user_from_token(request)
    user_id = -1 if user is None else user.id

    prompt_id = data.get("prompt_id")
    per_page = data.get("per_page", 30)
    page_index = data.get("page_index", 1)
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整, 缺少prompt_id")
    
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.BAD_REQUEST, "作品不存在")
    prompt = Prompt.objects.get(id=prompt_id)

    paginator = Paginator(prompt.comment_list.all().order_by("created_at"), per_page)
    page_comments = paginator.page(page_index)

    comment_list = []
    for comment in page_comments.object_list:
        comment_list.append(comment.full_dict(user_id=user_id))

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
        



