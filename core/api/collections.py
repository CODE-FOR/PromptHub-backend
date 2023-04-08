from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from .utils import response_wrapper, parse_data, failed_parse_data_response, check_data, failed_api_response, \
    StatusCode, success_api_response
from .auth import user_jwt_auth
from core.models.collection import Collection, CollectRecord, Prompt


'''
    add an item to collection
'''
@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def add_to_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    user = request.user
    collection_id = data.get("collection_id")
    prompt_id = data.get("prompt_id")

    if not check_data(user, collection_id, prompt_id):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    prompt = Prompt.objects.get(id=prompt_id)
    collection = Collection.objects.get(id=collection_id)

    if not check_data(prompt, collection):
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "无法收藏，数据异常")

    CollectRecord.objects.create(prompt=prompt, collection=collection)
    return success_api_response(msg="成功添加至收藏夹")


'''
    remove an item from collection
'''
@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def remove_from_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    id = data.get("id")

    if not check_data(id):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    collectRecord = CollectRecord.objects.get(id=id)
    collectRecord.delete()
    return success_api_response(msg="成功删除")


'''
    create a new collection
'''

@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def create_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    user = request.user
    name = data.get("name")
    visibility = data.get("visibility")
    cover = data.get("cover")

    if not check_data(name, visibility, cover):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if len(name) > 50:
        return failed_api_response(StatusCode.BAD_REQUEST, "名字过长")

    if Collection.objects.filter(name=name,user = user).exists():
        return failed_api_response(StatusCode.CONFLICT, "不可以使用重复的名字")

    Collection.objects.create(name=name, user=user, visibility=visibility,cover=cover)
    return success_api_response(msg="成功")


'''
    delete existing collection
'''
@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def delete_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    user = request.user
    collection_id = data.get("id")

    if not check_data(collection_id):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if not Collection.objects.filter(id=collection_id, user=user).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "数据异常")

    collection = Collection.objects.get(id=collection_id)
    collection.delete()
    return success_api_response(msg="成功删除收藏")


'''
    modify collection attribute
'''
@response_wrapper
@user_jwt_auth()
@require_http_methods("PUT")
def mod_collection(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    user = request.user
    collection_id = data.get("id")
    name = data.get("name")
    visibility = data.get("visibility")
    cover = data.get("cover")

    if not check_data(collection_id, name, visibility, cover):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if len(name) > 50:
        return failed_api_response(StatusCode.BAD_REQUEST, "名字过长")

    if Collection.objects.filter(name=name, user=user).exists():
        return failed_api_response(StatusCode.CONFLICT, "不可以使用重复的名字")

    collection = Collection.objects.get(id=collection_id)
    collection.name = name
    collection.visibility = visibility
    collection.cover = cover
    collection.save()

    return success_api_response(msg="成功更新收藏夹信息")