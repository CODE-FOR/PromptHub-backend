from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from core.models.user import User

@require_http_methods("GET")
def get_all_users(request: HttpRequest):
    users = User.objects.all()
    string = ""
    for user in users:
        string += user.nickname + "\n"
    return HttpResponse(string)
