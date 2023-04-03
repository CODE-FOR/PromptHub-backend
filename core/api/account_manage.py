from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from core.models.user import User, ConfirmCode

from .auth import user_jwt_auth
from .send_email import send_sign_in_email, send_forget_password_email
from .utils import StatusCode, response_wrapper, success_api_response, failed_api_responce, \
                   parse_data, failed_parse_data_response

@response_wrapper
@require_http_methods("POST")
def sign_up(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    email = data.get("email")
    if email is None:
        return failed_api_responce(StatusCode.BAD_REQUEST, "Need more infomation")
    if User.objects.filter(email=email).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Email already exists")
    
    send_sign_in_email(email)
    return success_api_response(msg="Verification code has been sent")

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
        return failed_api_responce(StatusCode.BAD_REQUEST, "Need more infomation")
    if User.objects.filter(email=email).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Email already exists")
    if User.objects.filter(nickname=nickname).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Nickname already exists")
    if not ConfirmCode.objects.filter(email=email).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Verification code has not been sent to this email")
    
    confirm_code = ConfirmCode.objects.get(email=email)
    if confirm_code.expire_at < timezone.now():
        return failed_api_responce(StatusCode.BAD_REQUEST, "Verification code expires")
    if code != confirm_code.code:
        return failed_api_responce(StatusCode.BAD_REQUEST, "Verification code is wrong")
    if confirm_code.is_used:
        return failed_api_responce(StatusCode.BAD_REQUEST, "Verification code has been used")
    confirm_code.is_used = True
    confirm_code.save()
    
    user = User.objects.create(
        email=email, password=password, nickname=nickname, is_confirmed=True
    )
    user.save()
    return success_api_response(msg="Successfully sign up")

@response_wrapper
@require_http_methods("POST")
def forget_password(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    email = data.get("email")
    if email is None:
        return failed_api_responce(StatusCode.BAD_REQUEST, "Need more infomation")
    if not User.objects.filter(email=email).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Email does not exist")
    
    send_forget_password_email(email)
    return success_api_response(msg="Verification code has been sent")

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
        return failed_api_responce(StatusCode.BAD_REQUEST, "Need more infomation")
    if not User.objects.filter(email=email).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Email does not exist")
    if not ConfirmCode.objects.filter(email=email).exists():
        return failed_api_responce(StatusCode.CONFLICT, "Verification code has not been sent to the email")
    
    confirm_code = ConfirmCode.objects.get(email=email)
    if confirm_code.expire_at < timezone.now():
        return failed_api_responce(StatusCode.BAD_REQUEST, "Verification code expires")
    if code != confirm_code.code:
        return failed_api_responce(StatusCode.BAD_REQUEST, "Verification code is wrong")
    if confirm_code.is_used:
        return failed_api_responce(StatusCode.BAD_REQUEST, "Verification code has been used")
    confirm_code.is_used = True
    confirm_code.save()
    
    user = User.objects.get(email=email)
    user.password = password
    user.save()
    return success_api_response(msg="Successfully change password")

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
        return failed_api_responce(StatusCode.BAD_REQUEST, "Old password is wrong")
    
    new_password = data.get("new_password")
    user.password = new_password
    user.save()
    return success_api_response(msg="Successfully change password")



