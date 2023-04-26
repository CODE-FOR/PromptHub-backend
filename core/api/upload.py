from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .auth import user_jwt_auth
from .utils import response_wrapper, success_api_response

from qiniu import Auth

import random
import string

ACCESS_KEY = 'brBbvVREpU769zgt11LTupGnPcO-5mtjB1WiNQu1'
SECRET_KEY = 'vasZWenWl_tzbDMOwbBOLCG5lUAJDN0KWGjhINFa'
QURIFY = Auth(ACCESS_KEY, SECRET_KEY)
BUCKET_NAME =  "prompthub2"


@response_wrapper
@user_jwt_auth()
@require_http_methods("GET")
def get_qiniu_token(request: HttpRequest):
    prefix = "".join(random.sample(string.ascii_letters + string.digits, 5))
    prefix += "_" + timezone.now().strftime("%y%m%d_%H%M%S")
    key = prefix + ".png"

    token = QURIFY.upload_token(BUCKET_NAME, key, 3600)

    return success_api_response(
        msg="成功获取token",
        data={
            "token": token,
            "key": key
        }
    )