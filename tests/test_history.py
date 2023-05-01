from tests.test_utils import *
from tests.data_history import *
from core.models.user import User
from core.models.prompt import Prompt
from core.models.history import History


class UserModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(HistoryTestData())
        self.client = TestClient(self.data)

    def test_get_history_list(self):
        user = User.objects.get(email=HISTORY_USER_EMAIL)
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "history_get_history_list",
            GET,
            {}
        ) \
        .check_code(200) \
        .check_contains("成功")
    
    def test_history_delete(self):
        user = User.objects.get(email=HISTORY_USER_EMAIL)
        prompt = Prompt.objects.get(prompt=HISTORY_PROMPT_ONE)
        history = History.objects.get(user=user, prompt=prompt)
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "history_delete_history",
            DELETE,
            {"history_id": history.id}
        ) \
        .check_code(200) \
        .check_contains("成功")
    
    def test_history_delete_fail(self):
        user = User.objects.get(email=HISTORY_USER_EMAIL)
        prompt = Prompt.objects.get(prompt=HISTORY_PROMPT_TWO)
        history = History.objects.get(user=user, prompt=prompt)
        self.client \
        .with_user_token(HISTORY_WRONG_USER_EMAIL) \
        .do_request(
            "history_delete_history",
            DELETE,
            {"history_id": history.id}
        ) \
        .check_code(400) \
        .check_contains("无权限")