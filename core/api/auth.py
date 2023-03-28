import json
import jwt
from datetime import timedelta, datetime

from django.conf import settings
from django.utils import timezone
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from .utils import StatusCode, failed_api_responce, success_api_response, response_wrapper

from core.models.user import User

def datetime_to_str(time: datetime) -> str:
    return datetime.strftime(time, "%Y-%m-%d %H:%M:%S.%f")


def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")


def auth_failed(message: str):
    return failed_api_responce(StatusCode.UNAUTHORIZED, message)


def generate_access_token(user_id: int, access_token_delta: int = 1) -> str:
    """
    user can use access_token to login
    Args:
        user_id: user.id
        access_token_delta: expiration time, unit: hour
    """
    cur_time = timezone.now()
    access_token_payload = {
        "user_id": user_id,
        "current_time": datetime_to_str(cur_time),
        "expiration_time": datetime_to_str(cur_time + timedelta(hours=access_token_delta)),
        "token_type": "access_token"
    }
    return jwt.encode(
        access_token_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def generate_refresh_token(user_id: int, refresh_token_delta: int = 0) -> str:
    """
    refresh_token has longer lifetime than access_token
    Args:
        user_id: user.id
        access_token_delta: expiration time, unit: hour
    """
    cur_time = timezone.now()
    refresh_token_payload = {
        "user_id": user_id,
        "current_time": datetime_to_str(cur_time),
        "expiration_time": datetime_to_str(cur_time + timedelta(hours=refresh_token_delta)),
        "token_type": "refresh_token"
    }
    return jwt.encode(
        refresh_token_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

@response_wrapper
@require_http_methods("POST")
def obtain_jwt_token(request: HttpRequest):
    data = json.loads(request.body.decode("utf-8"))
    # TODO check email & password valid
    email = data.get("email")
    password = data.get("password")
    return success_api_response(
        data={
            "access_token": generate_access_token(1),
            "refresh_token": generate_refresh_token(1)
        }
    )

@response_wrapper
@require_http_methods("GET")
def refresh_jwt_token(request: HttpRequest):
    """
    * if access_token expires but refresh_token does not expire
      then use refresh_token will generate a new access_token
    * if refresh_token expires then user need to re-login
    """
    try:
        header = request.META.get("HTTP_AUTHORIZATION")
        if header is None:
            raise jwt.InvalidTokenError

        # Authorization: Bearer <token>
        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        
        auth_type = auth_info[0]
        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        
        auth_token = auth_info[1]
        token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")

        if token.get("token_type") != "refresh_token":
            raise jwt.InvalidTokenError
        expiration_time = str_to_datetime(token.get("expiration_time"))
        if expiration_time < datetime.now():
            raise jwt.ExpiredSignatureError
        
        return success_api_response({"access_token": generate_access_token(token.get("user_id"))})
    except jwt.ExpiredSignatureError:
        return auth_failed("Token Expired")
    except jwt.InvalidTokenError:
        return auth_failed("Invalid Token")

def verify_jwt_token(request: HttpRequest) -> tuple(int, str):
    try:
        header = request.META.get("HTTP_AUTHORIZATION")
        if header is None:
            raise jwt.InvalidTokenError

        # Authorization: Bearer <token>
        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        
        auth_type = auth_info[0]
        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        
        auth_token = auth_info[1]
        token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")

        if token.get("token_type") != "access_token":
            raise jwt.InvalidTokenError
        expiration_time = str_to_datetime(token.get("expiration_time"))
        if expiration_time < datetime.now():
            raise jwt.ExpiredSignatureError
        return (token.get("user_id"), None)
    except jwt.ExpiredSignatureError:
        return (-1, "Token Expired")
    except jwt.InvalidTokenError:
        return (-1, "Invalid Token")

def jwt_auth():
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            user_id, message = verify_jwt_token(request)
            if user_id == -1:
                return auth_failed(message)
            user = User.objects.filter(pk=user_id, is_banned=False, is_delete=False).first()
            if user is None:
                return auth_failed("Account does not exist Or Account has been banned")
            request.user = user
            return func(request, *args, **kwargs)
        return wrapper
    return decorator