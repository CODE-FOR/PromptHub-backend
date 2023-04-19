from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from core.models.prompt import Prompt, LANCHED, UNDER_REVIEW
from core.models.audit_record import AuditRecord, IN_PROGRESS
from core.models.comment import Comment
from core.models.history import History

from .auth import user_jwt_auth, get_user_from_token
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

def new_audit_record(user, prompt):
    AuditRecord.objects.create(user=user, prompt=prompt, status=IN_PROGRESS, feedback="")

@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def create_prompt(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user

    prompt = data.get("prompt")
    picture = data.get("picture")
    picture = "img/" + picture
    model = data.get("model")
    width = data.get("width")
    height = data.get("height")
    prompt_attribute = data.get("prompt_attribute")
    upload_status = UNDER_REVIEW
    if prompt is None or picture is None or model is None or width is None \
    or height is None or prompt_attribute is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if len(prompt) > 4096 or len(picture) > 200 or len(model) > 256 \
        or len(prompt_attribute) > 4096:
        return failed_api_response(StatusCode.BAD_REQUEST, "内容过长")
    
    prompt_object = Prompt.objects.create(
        prompt=prompt, picture=picture, model=model, width=width, height=height,
        uploader=user, upload_status=upload_status, prompt_attribute=prompt_attribute
    )

    new_audit_record(user, prompt_object)

    return success_api_response(
        msg="成功上传作品, 等待审核",
        data={
            "id": prompt_object.id
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def edit_prompt(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user
    prompt_id = data.get("id")
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt_object = Prompt.objects.get(id=prompt_id)
    if user != prompt_object.uploader:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限修改该作品")
    
    prompt = data.get("prompt")
    picture = data.get("picture")
    model = data.get("model")
    width = data.get("width")
    height = data.get("height")
    prompt_attribute = data.get("prompt_attribute")
    if prompt is None or picture is None or model is None or width is None \
    or height is None or prompt_attribute is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if len(prompt) > 4096 or len(picture) > 200 or len(model) > 256 \
        or len(prompt_attribute) > 4096:
        return failed_api_response(StatusCode.BAD_REQUEST, "内容过长")
    
    prompt_object.prompt = prompt
    prompt_object.picture = picture
    prompt_object.model = model
    prompt_object.width = width
    prompt_object.height = height
    prompt_object.prompt_attribute = prompt_attribute
    prompt_object.upload_status = UNDER_REVIEW
    prompt_object.save()

    comment_list = Comment.objects.filter(prompt=prompt_object)
    for comment in comment_list:
        comment.delete()

    existing_in_progress_audit_record = AuditRecord.objects.filter(prompt=prompt_object, status=IN_PROGRESS)
    for audit_record in existing_in_progress_audit_record:
        audit_record.delete()

    new_audit_record(user, prompt_object)

    return success_api_response(
        msg="成功修改作品, 等待审核",
        data={
            "id": prompt_object.id
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("DELETE")
def delete_prompt(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user

    prompt_id = data.get("id")
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt_object = Prompt.objects.get(id=prompt_id)
    if user != prompt_object.uploader:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限删除该作品")
    prompt_object.delete()
    return success_api_response(
        msg="成功删除作品",
        data={
            "id": prompt_id
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_prompt(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    prompt_id = int(data.get("id"))
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt = Prompt.objects.get(id=prompt_id)

    if prompt.upload_status != LANCHED:
        return failed_api_response(StatusCode.BAD_REQUEST, "作品不存在")
    
    user = get_user_from_token(request)
    is_following = False
    if user is not None:
        uploader = prompt.uploader
        is_following = user.following.filter(following_user=uploader).exists()
    
    if user is not None:
        existing_histories = History.objects.filter(prompt=prompt, user=user)
        for history in existing_histories:
            history.delete()
        History.objects.create(prompt=prompt, user=user)

    return success_api_response(
        msg="成功获得作品内容",
        data={
            "prompt": prompt.full_dict(),
            "is_following": is_following
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_editing_prompt(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    prompt_id = int(data.get("id"))
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt = Prompt.objects.get(id=prompt_id)

    return success_api_response(
        msg="成功获得编辑作品详情",
        data={
            "prompt": prompt.full_dict()
        }
    )