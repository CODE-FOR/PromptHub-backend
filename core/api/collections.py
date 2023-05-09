from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from .utils import response_wrapper, parse_data, failed_parse_data_response, check_data, failed_api_response, \
    StatusCode, success_api_response
from .auth import user_jwt_auth, get_user_from_token
from core.models.collection import Collection, CollectRecord, Prompt, PUBLIC, PRIVATE
from core.models.prompt import LANCHED
from django.core.paginator import Paginator


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def manage_collection_records(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    user = request.user
    prompt_id = data.get("prompt_id")
    collection_list = data.get("collection_list")

    if not Prompt.objects.filter(id=prompt_id, upload_status=LANCHED).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="作品不存在")
    
    prompt = Prompt.objects.get(id=prompt_id, upload_status=LANCHED)
    for collection_info in collection_list:
        collection_id = collection_info["collection_id"]
        is_in = collection_info["is_in"]
        if not Collection.objects.filter(id=collection_id).exists():
            return failed_api_response(StatusCode.ID_NOT_EXISTS, error_msg="收藏夹不存在")
        collection = Collection.objects.get(id=collection_id)
        if collection.user != user:
            return failed_api_response(StatusCode.BAD_REQUEST, error_msg="用户无权限添加该收藏")
        
        if is_in and not CollectRecord.objects.filter(prompt=prompt, collection=collection).exists():
            prompt.collection_count = prompt.collection_count + 1
            CollectRecord.objects.create(prompt=prompt, collection=collection)
        elif not is_in and CollectRecord.objects.filter(prompt=prompt, collection=collection).exists():
            prompt.collection_count = prompt.collection_count + 1
            CollectRecord.objects.get(prompt=prompt, collection=collection).delete()
    prompt.save()
    
    return success_api_response(
        msg="成功更新作品收藏"
    )
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
    
    if user != collection.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限")

    CollectRecord.objects.create(prompt=prompt, collection=collection)
    
    collection.cover = prompt.picture
    collection.save()
    prompt.collection_count = prompt.collection_count + 1
    prompt.save()

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

    user = request.user
    id = data.get("id")

    if not check_data(id):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if not CollectRecord.objects.filter(id=id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "收藏记录不存在")
    collectRecord = CollectRecord.objects.get(id=id)

    if user != collectRecord.collection.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限")
    
    prompt = collectRecord.prompt
    prompt.collection_count = prompt.collection_count - 1
    prompt.save()
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

    if not check_data(name, visibility):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if len(name) > 50:
        return failed_api_response(StatusCode.BAD_REQUEST, "名字过长")

    if Collection.objects.filter(name=name, user=user).exists():
        return failed_api_response(StatusCode.CONFLICT, "不可以使用重复的名字")

    Collection.objects.create(name=name, user=user, visibility=visibility)
    return success_api_response(msg="成功创建")


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

    if user != collection.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限")
    
    collection.delete()
    return success_api_response(msg="成功删除收藏夹")


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
    collection = Collection.objects.get(id=collection_id)

    if not check_data(collection_id, name, visibility):
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if user != collection.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限")
    
    if len(name) > 50:
        return failed_api_response(StatusCode.BAD_REQUEST, "名字过长")

    if Collection.objects.filter(name=name, user=user).exists():
        c = Collection.objects.get(name=name, user=user)
        if c.id != collection_id:
            return failed_api_response(StatusCode.CONFLICT, "不可以使用重复的名字")

    collection.name = name
    collection.visibility = visibility
    collection.save()

    return success_api_response(msg="成功更新收藏夹信息")

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_collection_info(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    user = request.user
    collection_id = int(data.get("collection_id"))
    if not Collection.objects.filter(id=collection_id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "收藏夹不存在")
    collection = Collection.objects.get(id=collection_id)

    if user != collection.user:
        return failed_api_response(StatusCode.BAD_REQUEST, "用户无权限")

    return success_api_response(
        msg="成功获取收藏夹信息",
        data={
            "collection_info": collection.simple_dict()
        }
    )

@response_wrapper
@require_http_methods("GET")
def get_collection_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")

    user = get_user_from_token(request)
    user_id = -1 if user is None else user.id
    fetch_user_id = int(data.get("fetch_user_id"))

    if fetch_user_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整, 缺少fetch_user_id")
    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    collection_list = []
    if user_id == fetch_user_id:
        collection_list.extend(Collection.objects.filter(user_id=fetch_user_id))
    else:
        collection_list.extend(Collection.objects.filter(user_id=fetch_user_id, visibility=PUBLIC))

    collection_list_view = []
    paginator = Paginator(collection_list, per_page)
    page_collections = paginator.page(page_index)
    for collection in page_collections.object_list:
        collection_list_view.append(collection.full_dict())
    return success_api_response(
        msg="成功获取收藏列表",
        data={
            "collection_list": collection_list_view,
            "has_next": page_collections.has_next(),
            "has_previous": page_collections.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )


@response_wrapper
@require_http_methods("GET")
def get_collection_record_list(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")

    user = get_user_from_token(request)
    user_id = -1 if user is None else user.id
    
    collection_id = int(data.get("id"))
    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))
    collection_records_view = []

    if collection_id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    collection = Collection.objects.get(id=collection_id)
    if collection is None or (collection.visibility == PRIVATE and collection.user.id != user_id):
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "无此收藏夹或者不允许访问")

    collection_records = CollectRecord.objects.filter(collection_id=collection_id)
    paginator = Paginator(collection_records, per_page)
    page_records = paginator.page(page_index)

    for record in page_records:
        collection_records_view.append(record.full_dict())

    return success_api_response(
        msg="成功",
        data={
            "collection_record_list": collection_records_view,
            "has_next": page_records.has_next(),
            "has_previous": page_records.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_user_prompt_collection_relation(request: HttpRequest):
    data = request.GET.dict()
    if data is None:
        return failed_parse_data_response()
    
    prompt_id = int(data.get("prompt_id"))
    user = request.user

    if not Prompt.objects.filter(id=prompt_id):
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "作品不存在")
    prompt = Prompt.objects.get(id=prompt_id)

    prompt_collect_records = prompt.collect_list.all()
    prompt_collections = [record.collection for record in prompt_collect_records]
    collections = Collection.objects.filter(user_id=user.id)
    collection_list = []
    for collection in collections:
        collection_dict = collection.full_dict()
        prompt_is_in = False
        if collection in prompt_collections:
            prompt_is_in = True
        collection_dict["prompt_is_in"] = prompt_is_in
        collection_list.append(collection_dict)

    return success_api_response(
        msg="成功获取收藏列表",
        data={
            "collection_list": collection_list
        }
    )