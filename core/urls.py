"""
url routes of core apis
"""

from django.urls import path

import core.api.admin as admin
from core.api.auth import user_obtain_jwt_token, admin_obtain_jwt_token, refresh_jwt_token
from core.api.account_manage import sign_up, confirm_and_create, forget_password, confirm_forget_password, \
    change_password
from core.api.prompt import create_prompt, edit_prompt, delete_prompt, get_prompt
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
    path("admin/get_user_list", admin.get_user_list),
    path("admin/get_audit_record_list", admin.get_audit_record_list),
    path("admin/get_comment_list", admin.get_comment_list),
    path("admin/get_prompt_list", admin.get_prompt_list),
    path("admin/delete_comment", admin.delete_comment),
    path("admin/audit_prompt", admin.audit_prompt),

    # prompt apis
    path("prompt/create_prompt", create_prompt),
    path("prompt/edit_prompt", edit_prompt),
    path("prompt/delete_prompt", delete_prompt),
    path("prompt/get_prompt", get_prompt),

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
