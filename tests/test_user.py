from tests.test_utils import *
from tests.user_data import *


class UserModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData(), UserTestDataNotConfirmed(),
                            UserTestDataGotBanned())
        self.client = TestClient(self.data)

    def test_login(self):
        self.client.do_request("user_obtain_token",
                               POST, {
                                   'email': CORRECT_ACCOUNT_EMAIL,
                                   'password': CORRECT_ACCOUNT_PASSWORD
                               }).check_code(
            200).check_contains("成功")

    def test_login_error_code(self):
        self.client.do_request("user_obtain_token",
                               POST, {
                                   'email': CORRECT_ACCOUNT_EMAIL,
                                   'password': "error"
                               }).check_code(
            401).check_contains("密码错误")
