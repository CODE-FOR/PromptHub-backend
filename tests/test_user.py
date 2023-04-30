from tests.test_utils import *
from tests.user_data import *


class UserModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData(), UserTestDataNotConfirmed(),
                            UserTestDataGotBanned())
        self.client = TestClient(self.data)

    def test_login(self):
        self.client.do_request("auth_user_obtain_token",
                               POST, {
                                   'email': CORRECT_ACCOUNT_EMAIL,
                                   'password': CORRECT_ACCOUNT_PASSWORD
                               }).check_code(
            200).check_contains("成功")

    def test_login_error_code(self):
        self.client.do_request("auth_user_obtain_token",
                               POST, {
                                   'email': CORRECT_ACCOUNT_EMAIL,
                                   'password': "error"
                               }).check_code(
            401).check_contains("密码错误")

    def test_self_follow(self):
        self.client.with_user_token(CORRECT_NICK_NAME).do_request(
            "user_follow",
            POST, {
                'user_id': 1
            }
        ).check_contains("自己关注自己")
