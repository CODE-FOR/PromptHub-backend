from core.models.prompt import Prompt, LANCHED, UNDER_REVIEW
from core.models.user import User
from core.models.audit_record import AuditRecord, IN_PROGRESS
from tests.mock_data_set import DataProvider

PROMPT_USER_EMAIL = "prompt_user@user.com"
PROMPT_FOR_AUDIT_USER_EMAIL = "prompt_for_audit_user@user.com"


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


class PromptForAuditTestData(DataProvider):
    def set_data(self):
        user = User.objects.create(
            email=PROMPT_FOR_AUDIT_USER_EMAIL,
            password="prompt_for_audit_user",
            nickname="prompt_for_audit_user",
            is_confirmed=True
        )
        prompt_pass = Prompt.objects.create(
            prompt="prompt_for_audit_pass",
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
            prompt=prompt_pass,
            status=IN_PROGRESS,
            feedback=""
        )
        prompt_fail = Prompt.objects.create(
            prompt="prompt_for_audit_fail",
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
            prompt=prompt_fail,
            status=IN_PROGRESS,
            feedback=""
        )


class PromptForCollectionTestData(DataProvider):
    def set_data(self):
        user = User.objects.create(
            email=PROMPT_USER_EMAIL,
            password="prompt_user_for_collection",
            nickname="prompt_user_for_collection"
        )
        Prompt.objects.create(
            prompt="prompt_for_collection",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=LANCHED,
            prompt_attribute=""
        )
