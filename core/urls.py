"""
url routes of core apis
"""

from django.urls import path

from core.api.admin import get_all_users
from core.api.auth import user_obtain_jwt_token, admin_obtain_jwt_token, refresh_jwt_token
from core.api.account_manage import sign_up, confirm_and_create, forget_password, confirm_forget_password, \
    change_password
from core.api.comment import create_comment, delete_comment, get_comment_list
from core.api.collections import add_to_collection, create_collection, \
    delete_collection, mod_collection, remove_from_collection

urlpatterns = [
    # auth apis
    path("auth/user_obtain_token", user_obtain_jwt_token),
    path("auth/admin_obtain_token", admin_obtain_jwt_token),
    path("auth/refresh_token", refresh_jwt_token),

    # account apis
    path("user/sign_up", sign_up),
    path("user/confirm_and_create", confirm_and_create),
    path("user/forget_password", forget_password),
    path("user/confirm_forget_password", confirm_forget_password),
    path("user/change_password", change_password),

    # admin apis
    path("admin/get_all_users", get_all_users),

    # comment apis
    path("comment/create_comment", create_comment),
    path("comment/delete_comment", delete_comment),
    path("comment/get_comment_list/", get_comment_list),

    # collections apis —— for collection bundle
    path("collection/create_collection", create_collection),
    path("collection/delete_collection", delete_collection),
    path("collection/modify_collection", mod_collection),
    # collection apis —— for item
    path("collection/add_to_collection", add_to_collection),
    path("collection/remove_from_collection", remove_from_collection)

]
