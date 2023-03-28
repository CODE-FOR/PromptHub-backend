"""
url routes of core apis
"""

from django.urls import path

from core.api.admin import get_all_users
from core.api.auth import user_obtain_jwt_token, admin_obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    # admin apis
    path("admin_obtain_token", admin_obtain_jwt_token),
    path("all_users", get_all_users),

    # user apis
    path("user_obtain_token", user_obtain_jwt_token),

    # refresh token
    path("refresh_token", refresh_jwt_token)
]