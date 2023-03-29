"""
url routes of core apis
"""

from django.urls import path

from core.api.admin import get_all_users
from core.api.auth import user_obtain_jwt_token, admin_obtain_jwt_token, refresh_jwt_token
from core.api.account_manage import sign_up, confirm_and_create, forget_password, confirm_forget_password, change_password

urlpatterns = [
    # admin apis
    path("admin/obtain_token", admin_obtain_jwt_token),
    path("admin/get_all_users", get_all_users),

    # user apis
    path("user/obtain_token", user_obtain_jwt_token),
    path("user/sign_up", sign_up),
    path("user/confirm_and_create", confirm_and_create),
    path("user/forget_password", forget_password),
    path("user/confirm_forget_password", confirm_forget_password),
    path("user/change_password", change_password),

    # refresh token
    path("refresh_token", refresh_jwt_token)
]