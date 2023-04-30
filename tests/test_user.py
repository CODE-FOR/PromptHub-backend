from tests.test_utils import *
from tests.data_user import *


class UserModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData())
        self.client = TestClient(self.data)

    def test_self_follow(self):
        self.client.with_user_token(USER_EMAIL).do_request(
            "user_follow",
            POST, {
                'user_id': 1
            }
        ).check_contains("自己关注自己")
