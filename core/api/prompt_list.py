from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q

from core.models.prompt import Prompt, LANCHED
from core.models.history import History
import random

from .auth import get_user_from_token
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_response
from core.api.recommand import get_recommand_prompt_dict

@response_wrapper
@require_http_methods("GET")
def search_prompt_keyword(request: HttpRequest):
    data = request.GET.dict()
    if not data:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    keyword = data.get("keyword")
    sorted_by = data.get("sorted_by", "hot") # hot / time
    models = data.get("models", None)
    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    if models is None or len(models) == 0:
        prompt_list = Prompt.objects.filter(prompt__icontains=keyword, upload_status=LANCHED)
    else:
        models = models.split("_")
        complex_query = Q(model__icontains=models[0])
        for i in range(1, len(models)):
            complex_query = complex_query | Q(model__icontains=models[i])
        prompt_list = Prompt.objects.filter(prompt__icontains=keyword, upload_status=LANCHED).filter(complex_query)
        

    if sorted_by == "hot":
        prompt_list = prompt_list.order_by("-collection_count")
    else:
        prompt_list = prompt_list.order_by("-created_at")
    
    paginator = Paginator(prompt_list, per_page)
    page_prompt = paginator.page(page_index)

    search_prompt_list = []
    for prompt in page_prompt:
        search_prompt_list.append(prompt.simple_dict())
    
    return success_api_response(
        msg="搜索成功",
        data={
            "prompt_list": search_prompt_list,
            "has_next": page_prompt.has_next(),
            "has_previous": page_prompt.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@require_http_methods("GET")
def hot_prompt_list(request: HttpRequest):
    data = request.GET.dict()
    # if not data:
    #     return failed_api_response(StatusCode.BAD_REQUEST, "参数错误")
    
    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    prompt_list = Prompt.objects.filter(upload_status=LANCHED).order_by("-collection_count")
    
    paginator = Paginator(prompt_list, per_page)
    page_prompt = paginator.page(page_index)

    hot_prompt_list = []
    for prompt in page_prompt:
        hot_prompt_list.append(prompt.simple_dict())
    
    return success_api_response(
        msg="获取热门prompt成功",
        data={
            "prompt_list": hot_prompt_list,
            "has_next": page_prompt.has_next(),
            "has_previous": page_prompt.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )

@response_wrapper
@require_http_methods("GET")
def personized_prompt_list(request: HttpRequest):
    data = request.GET.dict()

    per_page = int(data.get("per_page", 30))
    page_index = int(data.get("page_index", 1))

    # random
    unsampled_prompt_list = Prompt.objects.filter(upload_status=LANCHED)
    count = unsampled_prompt_list.count()
    random.seed(100)
    random_list = random.sample(range(0, count), count)
    prompt_list = [unsampled_prompt_list[index] for index in random_list]
    
    paginator = Paginator(prompt_list, per_page)
    page_prompt = paginator.page(page_index)

    personized_prompt_list = []
    for prompt in page_prompt:
        personized_prompt_list.append(prompt.simple_dict())
    
    return success_api_response(
        msg="获取个性化prompt成功",
        data={
            "prompt_list": personized_prompt_list,
            "has_next": page_prompt.has_next(),
            "has_previous": page_prompt.has_previous(),
            "page_index": page_index,
            "page_total": paginator.num_pages
        }
    )