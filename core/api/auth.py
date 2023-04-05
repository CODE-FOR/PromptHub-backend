import jwt
from datetime import timedelta, datetime

from django.conf import settings
from django.utils import timezone
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from .utils import StatusCode, failed_api_responce, success_api_response, \
                   response_wrapper, failed_parse_data_response, parse_data

from core.models.admin import Admin
from core.models.user import User

ACCOUNT_TYPE_ADMIN = "admin"
ACCOUNT_TYPE_USER = "user"

def datetime_to_str(time: datetime) -> str:
    return datetime.strftime(time, "%Y-%m-%d %H:%M:%S.%f")


def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")


def auth_failed(message: str):
    return failed_api_responce(StatusCode.UNAUTHORIZED, message)


def generate_access_token(id: int, account_type: str, 
access_token_delta: int = 1) -> str:
    """
    account can use access_token to login
    Args:
        id: account id
        account_type: user or admin
        access_token_delta: expiration time, unit: hour
    """
    cur_time = timezone.now()
    access_token_payload = {
        "id": id,
        "current_time": datetime_to_str(cur_time),
        "expiration_time": datetime_to_str(cur_time + timedelta(hours=access_token_delta)),
        "token_type": "access_token",
        "account_type": account_type
    }
    return jwt.encode(
        access_token_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def generate_refresh_token(id: int, account_type: str, refresh_token_delta: int = 24) -> str:
    """
    refresh_token has longer lifetime than access_token
    Args:
        id: account id
        account_type: user or admin
        refresh_token_delta: expiration time, unit: hour
    """
    cur_time = timezone.now()
    refresh_token_payload = {
        "id": id,
        "current_time": datetime_to_str(cur_time),
        "expiration_time": datetime_to_str(cur_time + timedelta(hours=refresh_token_delta)),
        "token_type": "refresh_token",
        "account_type": account_type
    }
    return jwt.encode(
        refresh_token_payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

@response_wrapper
@require_http_methods("POST")
def user_obtain_jwt_token(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    email = data.get("email")
    password = data.get("password")
    
    if not User.objects.filter(email=email, is_banned=False, is_delete=False).exists():
        return auth_failed("Account does not exist or Account has been banned")
    user = User.objects.get(email=email)
        
    if user.password != password:
        return auth_failed("Wrong Password")
    
    return success_api_response(
        msg="Successfully obtain user tokens",
        data={
            "access_token": generate_access_token(user.id, ACCOUNT_TYPE_USER),
            "refresh_token": generate_refresh_token(user.id, ACCOUNT_TYPE_USER)
        }
    )

@response_wrapper
@require_http_methods("POST")
def admin_obtain_jwt_token(request: HttpRequest):
    data = parse_data(request)
    if data is None:
        return failed_parse_data_response()
    
    username = data.get("username")
    password = data.get("password")

    if not Admin.objects.filter(username=username).exists():
        return auth_failed("Account does not exist")
    admin = Admin.objects.get(username=username)

    if admin.password != password:
        return auth_failed("Wrong Password")
    
    return success_api_response(
        msg="Successfully obtain admin tokens",
        data={
            "access_token": generate_access_token(admin.id, ACCOUNT_TYPE_ADMIN),
            "refresh_token": generate_refresh_token(admin.id, ACCOUNT_TYPE_ADMIN)
        }
    )

@response_wrapper
@require_http_methods("GET")
def refresh_jwt_token(request: HttpRequest):
    """
    * if access_token expires but refresh_token does not expire
      then use refresh_token will generate a new access_token
    * if refresh_token expires then account need to re-login
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
        if expiration_time < timezone.now():
            raise jwt.ExpiredSignatureError
        
        return success_api_response(
            msg="Successfully refresh tokens",
            data={
                "access_token": generate_access_token(
                    token.get("id"),
                    token.get("account_type")
                )
            }
        )
                
    except jwt.ExpiredSignatureError:
        return auth_failed("Token Expired")
    except jwt.InvalidTokenError:
        return auth_failed("Invalid Token")

def verify_jwt_token(request: HttpRequest):
    """
    Returns:
        (id, message, account_type)
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

        if token.get("token_type") != "access_token":
            raise jwt.InvalidTokenError
        expiration_time = str_to_datetime(token.get("expiration_time"))
        if expiration_time < timezone.now():
            raise jwt.ExpiredSignatureError
        
        return (token.get("id"), None, token.get("account_type"))
    except jwt.ExpiredSignatureError:
        return (-1, "Token Expired", None)
    except jwt.InvalidTokenError:
        return (-1, "Invalid Token", None)

def user_jwt_auth():
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            id, message, account_type = verify_jwt_token(request)

            if id == -1:
                return auth_failed(message)
            
            if account_type != ACCOUNT_TYPE_USER:
                return auth_failed("Account has no permission")
            
            if not User.objects.filter(pk=id, is_banned=False, is_delete=False).exists():
                return auth_failed("Account does not exist Or Account has been banned")
            user = User.objects.get(pk=id, is_banned=False, is_delete=False)

            request.user = user
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_jwt_auth():
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            id, message, account_type = verify_jwt_token(request)

            if id == -1:
                return auth_failed(message)
            
            if account_type != ACCOUNT_TYPE_ADMIN:
                return auth_failed("Account has no permission")
            
            if not Admin.objects.filter(pk=id).exists():
                return auth_failed("Account does not exist")
            admin = Admin.objects.get(pk=id)

            request.user = admin
            return func(request, *args, **kwargs)
        return wrapper
    return decorator