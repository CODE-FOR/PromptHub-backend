from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from core.models.user import User, ConfirmCode
from .auth import user_jwt_auth
from .send_email import send_sign_in_email, send_forget_password_email
from .utils import StatusCode, response_wrapper, success_api_response, \
    failed_api_response, \
    parse_data, failed_parse_data_response


# this API maybe broken in future release @1330571 
@response_wrapper
@require_http_methods("GET")
def get_user_simple_dict(request: HttpRequest):
    data = request.GET.dict()
    if data is None:
        return failed_parse_data_response()
    id = data.get("id")
    if id is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not User.objects.filter(id=id).exists():
        return failed_api_response(StatusCode.ID_NOT_EXISTS, "没有此用户")
    user = User.objects.get(id=id)
    return success_api_response(msg="成功获取名字", data={
        "user": user.simple_dict()
    })


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def modify_user_info(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    nickname = data.get("nickname")
    avatar = data.get("avatar")
    user: User = request.user

    if nickname is None or avatar is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    avatar = avatar.replace("img/", "")
    avatar = "img/" + avatar

    user.nickname = nickname
    user.avatar = avatar
    user.save()

    return success_api_response(
        msg="用户信息修改成功",
        data={
            "user": user.simple_dict()
        }
    )


@response_wrapper
@require_http_methods("POST")
def sign_up(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    email = data.get("email")
    if email is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if User.objects.filter(email=email).exists():
        return failed_api_response(StatusCode.CONFLICT, "邮箱已注册")

    send_sign_in_email(email)
    return success_api_response(msg="验证码已发送")


@response_wrapper
@require_http_methods("PUT")
def confirm_and_create(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    email = data.get("email")
    password = data.get("password")
    nickname = data.get("nickname")
    code = data.get("code")

    if email is None or password is None or nickname is None or code is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if User.objects.filter(email=email).exists():
        return failed_api_response(StatusCode.CONFLICT, "邮箱已注册")
    if User.objects.filter(nickname=nickname).exists():
        return failed_api_response(StatusCode.CONFLICT, "用户名已存在")
    if not ConfirmCode.objects.filter(email=email).exists():
        return failed_api_response(StatusCode.CONFLICT,
                                   "还未向该邮箱发送过验证码")

    confirm_code = ConfirmCode.objects.get(email=email)
    if confirm_code.expire_at < timezone.now():
        return failed_api_response(StatusCode.BAD_REQUEST, "验证码过期")
    if code != confirm_code.code:
        return failed_api_response(StatusCode.BAD_REQUEST, "验证码错误")
    if confirm_code.is_used:
        return failed_api_response(StatusCode.BAD_REQUEST, "验证码已被使用")
    confirm_code.is_used = True
    confirm_code.save()

    User.objects.create(
        email=email, password=password, nickname=nickname, is_confirmed=True
    )
    return success_api_response(msg="成功注册")


@response_wrapper
@require_http_methods("POST")
def forget_password(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    email = data.get("email")
    if email is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not User.objects.filter(email=email).exists():
        return failed_api_response(StatusCode.CONFLICT, "邮箱不存在")

    send_forget_password_email(email)
    return success_api_response(msg="验证码已发送")


@response_wrapper
@require_http_methods("PUT")
def confirm_forget_password(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    email = data.get("email")
    password = data.get("password")
    code = data.get("code")

    if email is None or password is None or code is None:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")
    if not User.objects.filter(email=email).exists():
        return failed_api_response(StatusCode.CONFLICT, "邮箱不存在")
    if not ConfirmCode.objects.filter(email=email).exists():
        return failed_api_response(StatusCode.CONFLICT,
                                   "还未向该邮箱发送过验证码")

    confirm_code = ConfirmCode.objects.get(email=email)
    if confirm_code.expire_at < timezone.now():
        return failed_api_response(StatusCode.BAD_REQUEST, "验证码过期")
    if code != confirm_code.code:
        return failed_api_response(StatusCode.BAD_REQUEST, "验证码错误")
    if confirm_code.is_used:
        return failed_api_response(StatusCode.BAD_REQUEST, "验证码已被使用")
    confirm_code.is_used = True
    confirm_code.save()

    user = User.objects.get(email=email)
    user.password = password
    user.save()
    return success_api_response(msg="修改密码成功")


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def change_password(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    user = request.user
    old_password = data.get("old_password")
    if not user.check_password(old_password):
        return failed_api_response(StatusCode.BAD_REQUEST, "旧密码错误")

    new_password = data.get("new_password")
    user.password = new_password
    user.save()
    return success_api_response(msg="修改密码成功")


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def change_nickname(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    new_nickname = data.get("new_nickname")
    user_id = data.get("user_id")
    if not new_nickname or not user_id:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    if User.objects.filter(nickname=new_nickname).exists():
        return failed_api_response(StatusCode.CONFLICT,
                                   "昵称已经被使用了，换一个吧")

    user = request.user

    if user.id != int(user_id):
        return failed_api_response(StatusCode.FORBIDDEN, "无权限")

    user.nickname = new_nickname
    user.save()

    return success_api_response(msg="修改昵称成功")


@response_wrapper
@user_jwt_auth()
@require_http_methods("POST")
def change_avatar(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()

    new_avatar = data.get("new_avatar")
    user_id = data.get("user_id")
    if not new_avatar:
        return failed_api_response(StatusCode.BAD_REQUEST, "参数不完整")

    user = request.user

    if user.id != int(user_id):
        return failed_api_response(StatusCode.FORBIDDEN, "无权限")

    user.avatar = new_avatar
    user.save()

    return success_api_response(msg="头像修改成功")
