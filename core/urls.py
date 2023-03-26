"""
url routes of core apis
"""

from django.urls import path

from core.api.admin import get_all_users

urlpatterns = [
    # admin apis
    path("all_users", get_all_users)
]