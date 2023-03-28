"""
url routes of core apis
"""

from django.urls import path

from core.api.admin import get_all_users
from core.api.auth import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    # admin apis
    path("all_users", get_all_users),

    # user apis
    path("obtain_token", obtain_jwt_token),
    path("refresh_token", refresh_jwt_token)
]