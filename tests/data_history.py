from core.models.user import User
from core.models.history import History
from core.models.prompt import Prompt, LANCHED

from tests.mock_data_set import DataProvider

HISTORY_USER_EMAIL = "history_user@user.com"
HISTORY_WRONG_USER_EMAIL = "history_wrong_user@user.com"
HISTORY_PROMPT_ONE = "special_for_history_prompt_one"
HISTORY_PROMPT_TWO = "special_for_history_prompt_two"

class HistoryTestData(DataProvider):
    def set_data(self):
        User.objects.create(
            email=HISTORY_WRONG_USER_EMAIL,
            password="history_user",
            nickname="history_user"
        )
        user = User.objects.create(
            email=HISTORY_USER_EMAIL,
            password="history_user",
            nickname="history_user"
        )
        prompt_one = Prompt.objects.create(
            prompt=HISTORY_PROMPT_ONE,
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=LANCHED,
            prompt_attribute=""
        )
        prompt_two = Prompt.objects.create(
            prompt=HISTORY_PROMPT_TWO,
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=LANCHED,
            prompt_attribute=""
        )
        History.objects.create(
            user=user,
            prompt=prompt_one
        )
        History.objects.create(
            user=user,
            prompt=prompt_two
        )

