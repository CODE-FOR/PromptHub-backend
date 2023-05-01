from core.models.user import User
from core.models.comment import Comment
from core.models.prompt import Prompt, LANCHED

from tests.mock_data_set import DataProvider

COMMENT_USER_EMAIL = "comment_user@user.com"
COMMENT_PROMPT_PROMPT = "special_for_comment_prompt"
COMMENT_COMMENT_DELETE = "special_for_comment_delete"

class CommentTestData(DataProvider):
    def set_data(self):
        user = User.objects.create(
            email=COMMENT_USER_EMAIL,
            password="comment_user",
            nickname="comment_user"
        )
        prompt = Prompt.objects.create(
            prompt=COMMENT_PROMPT_PROMPT,
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=LANCHED,
            prompt_attribute=""
        )
        Comment.objects.create(
            prompt=prompt,
            user=user,
            content=COMMENT_COMMENT_DELETE
        )

