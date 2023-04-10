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
from core.api.history import get_history_list, delete_history
from core.api.collections import add_to_collection, create_collection, \
    delete_collection, mod_collection, remove_from_collection, get_collection_list, get_collection_record_list
from core.api.notification import get_notification_list, delete_notification, update_notification, \
    get_unread_notification_num
from core.api.prompt_list import search_prompt_keyword, hot_prompt_list, personized_prompt_list
from core.api.user import follow, get_self_published_prompt, get_audit_record_list, delete_audit_record

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

    # user profile apis
    path("user/follow", follow),
    path("user/get_prompt_list", get_self_published_prompt),
    path("user/get_audit_record_list", get_audit_record_list),
    path("user/delete_audit_record", delete_audit_record),

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
    path("comment/get_comment_list", get_comment_list),

    # history apis
    path("history/get_history_list", get_history_list),
    path("history/delete_history", delete_history),

    # collections apis —— for collection bundle
    path("collection/create_collection", create_collection),
    path("collection/delete_collection", delete_collection),
    path("collection/modify_collection", mod_collection),
    path("collection/get_collection_list", get_collection_list),
    # collection apis —— for item
    path("collection/add_to_collection", add_to_collection),
    path("collection/remove_from_collection", remove_from_collection),
    path("collection/get_collection_record_list", get_collection_record_list),

    # notification apis
    path("notification/get_notification_list", get_notification_list),
    path("notification/delete_notification", delete_notification),
    path("notification/update_notification", update_notification),
    path("notification/get_unread_notification_num", get_unread_notification_num),

    # prompt_list
    path("prompt_list/search_prompt_keyword", search_prompt_keyword),
    path("prompt_list/hot_prompt_list", hot_prompt_list),
    path("prompt_list/personized_prompt_list", personized_prompt_list)
]
