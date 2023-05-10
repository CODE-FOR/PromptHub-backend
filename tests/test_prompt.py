from tests.test_utils import *
from tests.data_user import *
from tests.data_prompt import *

class PromptModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData(),
                            PromptOneTestData(),
        )
        self.client = TestClient(self.data)

    def test_create_prompt(self):
        self.client.with_user_token(USER_EMAIL).do_request(
            "prompt_create_prompt",
            POST, {"prompt": "prompt", "picture": "picture.jpg", "model": "model", "width": 512, "height": 512, "prompt_attribute": ""}
        ).check_contains("成功").check_code(200)

    def test_edit_prompt(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.with_user_token(PROMPT_USER_EMAIL).do_request(
            "prompt_edit_prompt",
            POST, {"id": prompt.id, "prompt": "prompt", "picture": "picture.jpg", "model": "model", "width": 512, "height": 512, "prompt_attribute": ""}
        ).check_contains("成功").check_code(200)

    def test_get_prompt(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.do_request(
            "prompt_get_prompt",
            GET,
            {
                "id": prompt.id
            }
        ).check_code(200).check_contains("成功")

    def test_edit_prompt_fail(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.with_user_token(USER_EMAIL).do_request(
            "prompt_edit_prompt",
            POST, {"id": prompt.id, "prompt": "prompt", "picture": "picture.jpg", "model": "model", "width": 512, "height": 512, "prompt_attribute": ""}
        ).check_contains("无权限").check_code(400)


    def test_delete_prompt_fail(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.with_user_token(USER_EMAIL).do_request(
            "prompt_delete_prompt",
            DELETE, {"id": prompt.id}
        ).check_contains("无权限").check_code(400)

    def test_get_editing_prompt(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.with_user_token(PROMPT_USER_EMAIL).do_request(
            "prompt_get_editing_prompt",
            GET, {"id": prompt.id}
        ).check_contains("成功").check_code(200)

    def test_get_editing_prompt_fail(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.with_user_token(USER_EMAIL).do_request(
            "prompt_get_editing_prompt",
            GET, {"id": prompt.id}
        ).check_contains("无权限").check_code(400)

    def test_delete_prompt(self):
        user = User.objects.filter(email=PROMPT_USER_EMAIL)[0]
        prompt = Prompt.objects.filter(uploader=user)[0]
        self.client.with_user_token(PROMPT_USER_EMAIL).do_request(
            "prompt_delete_prompt",
            DELETE, {"id": prompt.id}
        ).check_contains("成功").check_code(200)