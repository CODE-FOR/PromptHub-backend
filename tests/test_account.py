from tests.test_utils import *
from tests.data_user import *
from core.models.user import ConfirmCode

SIGN_UP_USER_EMAIL = "sign_up@sign.up"
SIGN_UP_USER_PASSWORD = "sign_up"
SIGN_UP_USER_NICKNAME = "sign_up"

class AccountModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData())
        self.client = TestClient(self.data)
    
    def test_get_user_info(self):
        self.client \
            .do_request(
                "user_get_user_simple_dict", 
                GET,
                {"id": 1}
            ) \
            .check_code(200) \
            .check_contains("成功")

    def test_get_nonexistent_user_info(self):
        self.client \
            .do_request(
                "user_get_user_simple_dict", 
                GET,
                {"id": -1}
            ) \
            .check_code(555) \
            .check_contains("没有")
    
    def test_user_sign_up(self):
        # test user_sign_up
        self.client \
            .do_request(
                "user_sign_up",
                POST,
                {"email": SIGN_UP_USER_EMAIL}
            ) \
            .check_code(200) \
            .check_contains("已发送")
        # test user_confirm_and_create
        confirm_code = ConfirmCode.objects.get(email=SIGN_UP_USER_EMAIL)
        self.client \
            .do_request(
                "user_confirm_and_create",
                PUT,
                {
                    "email": SIGN_UP_USER_EMAIL,
                    "password": SIGN_UP_USER_PASSWORD,
                    "nickname": SIGN_UP_USER_NICKNAME,
                    "code": confirm_code.code
                }
            ) \
            .check_code(200) \
            .check_contains("成功")
    
    def test_user_already_sign_up(self):
        self.client \
            .do_request(
                "user_sign_up",
                POST,
                {"email": USER_EMAIL}
            ) \
            .check_code(409) \
            .check_contains("已注册")
    
    def test_user_find_password(self):
        # test user_forget_password
        self.client \
            .do_request(
                "user_forget_password",
                POST,
                {"email": USER_EMAIL}
            ) \
            .check_code(200) \
            .check_contains("已发送")
        # test user_confirm_forget_password
        confirm_code = ConfirmCode.objects.get(email=USER_EMAIL)
        self.client \
            .do_request(
                "user_confirm_forget_password",
                PUT,
                {
                    "email": USER_EMAIL,
                    "password": USER_PASSWORD,
                    "code": confirm_code.code
                }
            ) \
            .check_code(200) \
            .check_contains("成功")
    
    def test_user_change_password(self):
        self.client \
            .with_user_token(USER_EMAIL) \
            .do_request(
                "user_change_password",
                POST,
                {
                    "old_password": USER_PASSWORD,
                    "new_password": USER_PASSWORD
                }
            ) \
            .check_code(200) \
            .check_contains("成功")
    
    def test_user_change_avatar(self):
        user = User.objects.get(email=USER_EMAIL)
        self.client \
            .with_user_token(USER_EMAIL) \
            .do_request(
                "user_change_avatar",
                POST,
                {
                    "new_avatar": USER_AVATAR,
                    "user_id": user.id,
                }
            ) \
            .check_code(200) \
            .check_contains("成功")
    
    def test_user_change_nickname(self):
        user = User.objects.get(email=USER_EMAIL)
        self.client \
            .with_user_token(USER_EMAIL) \
            .do_request(
                "user_change_nickname",
                POST,
                {
                    "new_nickname": "new_nickname",
                    "user_id": user.id,
                }
            ) \
            .check_code(200) \
            .check_contains("成功")
        self.client \
            .with_user_token(USER_EMAIL) \
            .do_request(
                "user_change_nickname",
                POST,
                {
                    "new_nickname": USER_NICKNAME,
                    "user_id": user.id,
                }
            ) \
            .check_code(200) \
            .check_contains("成功")