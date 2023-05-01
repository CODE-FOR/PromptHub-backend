from tests.test_utils import *
from tests.data_comment import *
from core.models.user import User
from core.models.prompt import Prompt
from core.models.comment import Comment


class UserModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(CommentTestData())
        self.client = TestClient(self.data)

    def test_comment_create(self):
        user = User.objects.get(email=COMMENT_USER_EMAIL)
        prompt = Prompt.objects.get(prompt=COMMENT_PROMPT_PROMPT)
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "comment_create_comment",
            POST,
            {"prompt_id": prompt.id, "content": "好看"}
        ) \
        .check_code(200) \
        .check_contains("成功")
    
    def test_comment_delete(self):
        user = User.objects.get(email=COMMENT_USER_EMAIL)
        comment = Comment.objects.get(content=COMMENT_COMMENT_DELETE)
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "comment_delete_comment",
            DELETE,
            {"comment_id": comment.id}
        ) \
        .check_code(200) \
        .check_contains("成功")
    
    def test_comment_delete_fail(self):
        user = User.objects.get(email=COMMENT_USER_EMAIL)
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "comment_delete_comment",
            DELETE,
            {"comment_id": -1}
        ) \
        .check_code(555) \
        .check_contains("不存在")

    def test_get_comment_list(self):
        prompt = Prompt.objects.get(prompt=COMMENT_PROMPT_PROMPT)
        self.client \
        .do_request(
            "comment_get_comment_list",
            GET,
            {"prompt_id": prompt.id}
        ) \
        .check_code(200) \
        .check_contains("成功")