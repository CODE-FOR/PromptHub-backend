from tests.test_utils import *
from tests.data_admin import *
from tests.data_prompt import *
from tests.data_comment import *

class AdminModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(AdminTestData(),
                            PromptForAuditTestData(),
                            CommentTestData()
        )
        self.client = TestClient(self.data)

    
    def test_get_user_list(self):
        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_get_user_list",
            GET, {}
        ).check_contains("成功").check_code(200)

    def test_get_prompt_list(self):
        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_get_prompt_list",
            GET, {}
        ).check_contains("成功").check_code(200)

    def test_get_audit_record_list(self):
        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_get_audit_record_list",
            GET, {}
        ).check_contains("成功").check_code(200)

    def test_get_prompt(self):
        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_get_prompt",
            GET, {"prompt_id": 1}
        ).check_contains("成功").check_code(200)

    def test_audit_prompt(self):
        audit_prompt = Prompt.objects.filter(prompt="prompt_for_audit_pass")[0]
        audit_record = AuditRecord.objects.filter(prompt=audit_prompt)[0]

        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_audit_prompt",
            POST, {"id": audit_record.id, "passed": True, "cotent": ""}
        ).check_contains("完成").check_code(200)

    def test_audit_prompt_fail(self):
        audit_prompt = Prompt.objects.filter(prompt="prompt_for_audit_fail")[0]
        audit_record = AuditRecord.objects.filter(prompt=audit_prompt)[0]

        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_audit_prompt",
            POST, {"id": audit_record.id, "passed": False, "cotent": ""}
        ).check_contains("完成").check_code(200)

    def test_get_comment_list(self):
        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_get_comment_list",
            GET, {"prompt_id": 1}
        ).check_contains("成功").check_code(200)

    def test_delete_comment(self):
        comment_user = User.objects.get(email=COMMENT_USER_EMAIL)
        comment = Comment.objects.filter(user=comment_user)[0]

        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_delete_comment",
            DELETE, {"comment_id": comment.id}
        ).check_contains("成功").check_code(200)