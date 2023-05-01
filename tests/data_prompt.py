from core.models.user import User
from core.models.prompt import Prompt, LANCHED
from tests.mock_data_set import DataProvider

PROMPT_USER_EMAIL = "prompt_user@user.com"

class PromptOneTestData(DataProvider):
    def set_data(self):
        user = User.objects.create(
            email=PROMPT_USER_EMAIL,
            password="prompt_user",
            nickname="prompt_user"
        )
        Prompt.objects.create(
            prompt="prompt_1",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=LANCHED,
            prompt_attribute=""
        )
