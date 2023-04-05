from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from core.models.user import User
from .utils import response_wrapper, success_api_response

from .auth import admin_jwt_auth

@response_wrapper
@admin_jwt_auth()
@require_http_methods("GET")
def get_all_users(request: HttpRequest):
    users = User.objects.all()
    string = ""
    for user in users:
        string += user.nickname + "\n"
    return success_api_response(msg="Success", data={"name": string})
