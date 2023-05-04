from core.models.prompt import Prompt, LANCHED, UNDER_REVIEW
from core.models.user import User
from core.models.audit_record import AuditRecord, IN_PROGRESS
from tests.mock_data_set import DataProvider

PROMPT_LIST_USER_EMAIL = "prompt_list_user@user.com"


class PromptListTestData(DataProvider):
    def set_data(self):
        user = User.objects.create(
            email=PROMPT_LIST_USER_EMAIL,
            password="prompt_user",
            nickname="prompt_user"
        )
        for i in range(10):
            Prompt.objects.create(
                prompt="prompt_list_" + str(i),
                picture="picture.jpg",
                model="model",
                width=512,
                height=512,
                uploader=user,
                upload_status=LANCHED,
                collection_count=i,
                prompt_attribute=""
            )
        
