from core.models.user import User
from core.models.audit_record import AuditRecord
from core.models.prompt import Prompt, UNDER_REVIEW
from tests.mock_data_set import DataProvider

RECORD_USER_EMAIL = "record_user@user.com"

class AuditTestData(DataProvider):
    def set_data(self):
        user = User.objects.create(
            email=RECORD_USER_EMAIL,
            password="record_user",
            nickname="record_user"
        )
        prompt = Prompt.objects.create(
            prompt="prompt_2",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=UNDER_REVIEW,
            prompt_attribute=""
        )
        AuditRecord.objects.create(
            user=user,
            prompt=prompt,
            status=UNDER_REVIEW,
            feedback=""
        )

