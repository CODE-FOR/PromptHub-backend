"""
url routes of core apis
"""

from django.urls import path

import core.api.admin as admin
from core.api.account_manage import sign_up, get_user_simple_dict, \
    confirm_and_create, forget_password, confirm_forget_password, \
    change_password, change_avatar, change_nickname
from core.api.auth import user_obtain_jwt_token, admin_obtain_jwt_token, \
    refresh_jwt_token
from core.api.collections import add_to_collection, create_collection, \
    delete_collection, mod_collection, remove_from_collection, \
    get_collection_list, get_collection_record_list, \
    get_user_prompt_collection_relation, manage_collection_records, \
    get_collection_info
from core.api.comment import create_comment, delete_comment, get_comment_list
from core.api.history import get_history_list, delete_history
from core.api.notification import get_notification_list, delete_notification, \
    update_notification, \
    get_unread_notification_num
from core.api.prompt import create_prompt, edit_prompt, delete_prompt, \
    get_prompt, get_editing_prompt
from core.api.prompt_list import search_prompt_keyword, hot_prompt_list, \
    personized_prompt_list
from core.api.upload import get_qiniu_token
from core.api.user import follow, get_published_prompt_list, \
    get_audit_record_list, delete_audit_record, \
    get_user_following_num, get_user_following_list, get_user_follower_num, \
    get_user_follower_list, \
    get_published_prompt_num, is_following

urlpatterns = [
    # auth apis
    path("auth/user_obtain_token", user_obtain_jwt_token,
         name="auth_user_obtain_token"),
    path("auth/admin_obtain_token", admin_obtain_jwt_token,
         name="auth_admin_obtain_token"),
    path("auth/refresh_token", refresh_jwt_token,
         name="auth_refresh_token"),

    # account apis
    path("user/get_user_simple_dict", get_user_simple_dict,
         name="user_get_user_simple_dict"),
    path("user/sign_up", sign_up, name="user_sign_up"),
    path("user/confirm_and_create", confirm_and_create,
         name="user_confirm_and_create"),
    path("user/forget_password", forget_password, name="user_forget_password"),
    path("user/confirm_forget_password", confirm_forget_password,
         name="user_confirm_forget_password"),
    path("user/change_password", change_password, name="user_change_password"),
    # path("user/modify_user_info", modify_user_info),
    path("user/change_avatar", change_avatar, name="user_change_avatar"),
    path("user/change_nickname", change_nickname, name="user_change_nickname"),

    # user profile apis
    path("user/follow", follow, name="user_follow"),
    path("user/get_user_following_num", get_user_following_num,
         name="user_get_user_following_num"),
    path("user/get_user_following_list", get_user_following_list,
         name="user_get_user_following_list"),
    path("user/get_user_follower_num", get_user_follower_num,
         name="user_get_user_follower_num"),
    path("user/get_user_follower_list", get_user_follower_list,
         name="user_get_user_follower_list"),
    path("user/get_published_prompt_num", get_published_prompt_num,
         name="user_get_published_prompt_num"),
    path("user/get_published_prompt_list", get_published_prompt_list,
         name="user_get_published_prompt_list"),
    path("user/get_audit_record_list", get_audit_record_list,
         name="user_get_audit_record_list"),
    path("user/delete_audit_record", delete_audit_record,
         name="user_delete_audit_record"),
    path("user/is_following", is_following, name="user_is_following"),

    # admin apis
    path("admin/get_user_list", admin.get_user_list,
         name="admin_get_user_list"),
    path("admin/get_audit_record_list", admin.get_audit_record_list,
         name="admin_get_audit_record_list"),
    path("admin/get_comment_list", admin.get_comment_list,
         name="admin_get_comment_list"),
    path("admin/get_prompt_list", admin.get_prompt_list,
         name="admin_get_prompt_list"),
    path("admin/delete_comment", admin.delete_comment,
         name="admin_delete_comment"),
    path("admin/audit_prompt", admin.audit_prompt, name="admin_audit_prompt"),
    path("admin/get_prompt", admin.get_prompt, name="admin_get_prompt"),

    # prompt apis
    path("prompt/create_prompt", create_prompt, name="prompt_create_prompt"),
    path("prompt/edit_prompt", edit_prompt, name="prompt_edit_prompt"),
    path("prompt/delete_prompt", delete_prompt, name="prompt_delete_prompt"),
    path("prompt/get_prompt", get_prompt, name="prompt_get_prompt"),
    path("prompt/get_editing_prompt", get_editing_prompt,
         name="prompt_get_editing_prompt"),

    # comment apis
    path("comment/create_comment", create_comment,
         name="comment_create_comment"),
    path("comment/delete_comment", delete_comment,
         name="comment_delete_comment"),
    path("comment/get_comment_list", get_comment_list,
         name="comment_get_comment_list"),

    # history apis
    path("history/get_history_list", get_history_list,
         name="history_get_history_list"),
    path("history/delete_history", delete_history,
         name="history_delete_history"),

    # collections apis —— for collection bundle
    path("collection/create_collection", create_collection,
         name="collection_create_collection"),
    path("collection/delete_collection", delete_collection,
         name="collection_delete_collection"),
    path("collection/modify_collection", mod_collection,
         name="collection_mod_collection"),
    path("collection/get_collection_list", get_collection_list,
         name="collection_get_collection_list"),
    path("collection/get_collection_info", get_collection_info,
         name="collection_get_collection_info"),
    # collection apis —— for item
    path("collection/manage_collection_records", manage_collection_records,
         name="collection_manage_collection_records"),
    path("collection/add_to_collection", add_to_collection,
         name="collection_add_to_collection"),
    path("collection/remove_from_collection", remove_from_collection,
         name="collection_remove_from_collection"),
    path("collection/get_collection_record_list", get_collection_record_list,
         name="collection_get_collection_record_list"),
    # collection other api
    path("collection/get_user_prompt_collection_relation",
         get_user_prompt_collection_relation,
         name="collection_get_user_prompt_collection_relation"),

    # notification apis
    path("notification/get_notification_list", get_notification_list,
         name="notification_get_notification_list"),
    path("notification/delete_notification", delete_notification,
         name="notification_delete_notification"),
    path("notification/update_notification", update_notification,
         name="notification_update_notification"),
    path("notification/get_unread_notification_num",
         get_unread_notification_num,
         name="notification_get_unread_notification_num"),

    # prompt_list
    path("prompt_list/search_prompt_keyword", search_prompt_keyword,
         name="prompt_list_search_prompt_keyword"),
    path("prompt_list/hot_prompt_list", hot_prompt_list,
         name="prompt_list_hot_prompt_list"),
    path("prompt_list/personized_prompt_list", personized_prompt_list,
         name="prompt_list_personalized_prompt_list"),

    # upload image
    path("image/get_qiniu_token", get_qiniu_token, name="image_get_qiniu_token")

]
