from tests.test_utils import *
from tests.data_admin import *
from tests.data_user import *


class AuthModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(AdminTestData(), 
                            UserTestData(), 
                            UserTestDataNotConfirmed(),
                            UserTestDataGotBanned())
        self.client = TestClient(self.data)

    def test_user_login(self):
        self.client.do_request("auth_user_obtain_token",
                               POST, {
                                   'email': USER_EMAIL,
                                   'password': USER_PASSWORD
                               }).check_code(
            200).check_contains("成功")
        
    def test_user_login_error_code(self):
        self.client.do_request("auth_user_obtain_token",
                               POST, {
                                   'email': USER_EMAIL,
                                   'password': "error"
                               }).check_code(
            401).check_contains("密码错误")
        
    def test_admin_login(self):
        self.client.do_request("auth_admin_obtain_token",
                               POST, {
                                   'username': ADMIN_USERNAME,
                                   'password': ADMIN_PASSWORD
                               }).check_code(
            200).check_contains("成功")
    
    def test_admin_refresh_token(self):
        self.client \
            .with_admin_refresh_token(ADMIN_USERNAME) \
            .do_request("auth_refresh_token", GET, {}) \
            .check_code(200) \
            .check_contains("成功")
