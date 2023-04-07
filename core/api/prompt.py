from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from core.models.prompt import Prompt

from .auth import user_jwt_auth
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response, \
                   parse_data, failed_parse_data_response

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
    model = data.get("model")
    width = data.get("width")
    height = data.get("height")
    prompt_attribute = data.get("prompt_attribute")
    upload_status = 1
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
    
    prompt_object.prompt = data.get("prompt")
    prompt_object.picture = data.get("picture")
    prompt_object.model = data.get("model")
    prompt_object.width = data.get("width")
    prompt_object.height = data.get("height")
    prompt_object.prompt_attribute = data.get("prompt_attribute")
    prompt_object.upload_status = 1
    prompt_object.save()

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
            "id": prompt_object.id
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_prompt(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    prompt_id = data.get("id")
    if prompt_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not Prompt.objects.filter(id=prompt_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt = Prompt.objects.get(id=prompt_id)

    if prompt.upload_status != 0:
        return failed_api_response(StatusCode.BAD_REQUEST, "作品已下架")

    return success_api_response(
        msg="成功获得作品内容",
        data={
            "prompt": prompt.full_dict()
        }
    )