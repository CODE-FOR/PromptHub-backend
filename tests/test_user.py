from tests.test_utils import *
from tests.data_user import *
from tests.data_prompt import *
from tests.data_record import *


class UserModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData(), 
                            UserTestTwoData(), 
                            PromptOneTestData(), 
                            AuditTestData())
        self.client = TestClient(self.data)

    def test_self_follow(self):
        self.client.with_user_token(USER_EMAIL).do_request(
            "user_follow",
            POST, {
                'user_id': 1
            }
        ).check_contains("自己关注自己")
    
    def test_follow(self):
        user_one = User.objects.get(email="test@test.com")
        user_two = User.objects.get(email="test_2@test.com")
        # test user_follow
        self.client \
        .with_user_token(user_one.email) \
        .do_request(
            "user_follow",
            POST,
            {"user_id": user_two.id}
        ) \
        .check_code(200) \
        .check_contains("成功")
        # test user_is_following
        self.client \
        .with_user_token(user_one.email) \
        .do_request(
            "user_is_following",
            GET,
            {"target_user_id": user_two.id}
        )
    
    def test_get_user_following(self):
        user_one = User.objects.get(email="test@test.com")
        # test user_get_user_following_num
        self.client \
        .do_request(
            "user_get_user_following_num",
            GET,
            {"user_id": user_one.id}
        ) \
        .check_code(200) \
        .check_contains("成功获取关注人数")
        # test user_get_user_following_list
        self.client \
        .do_request(
            "user_get_user_following_list",
            GET,
            {"user_id": user_one.id}
        ) \
        .check_code(200) \
        .check_contains("成功获取关注列表")

    def test_get_user_follower(self):
        user_two = User.objects.get(email="test_2@test.com")
        # test user_get_user_follower_num
        self.client \
        .do_request(
            "user_get_user_follower_num",
            GET,
            {"user_id": user_two.id}
        ) \
        .check_code(200) \
        .check_contains("成功获取粉丝人数")
        # test user_get_user_follower_list
        self.client \
        .do_request(
            "user_get_user_follower_list",
            GET,
            {"user_id": user_two.id}
        ) \
        .check_code(200) \
        .check_contains("成功获取粉丝列表")

    def test_get_user_prompt(self):
        user = User.objects.get(email=PROMPT_USER_EMAIL)
        # test user_get_published_prompt_num
        self.client \
        .do_request(
            "user_get_published_prompt_num",
            GET,
            {"user_id": user.id}
        ) \
        .check_code(200) \
        .check_contains("成功获取作品数量")
        # test user_get_published_prompt_list
        self.client \
        .do_request(
            "user_get_published_prompt_list",
            GET,
            {"user_id": user.id}
        ) \
        .check_code(200) \
        .check_contains("成功获取Prompt")

    def test_get_user_record(self):
        user = User.objects.get(email=RECORD_USER_EMAIL)
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "user_get_audit_record_list",
            GET,
            {}
        ) \
        .check_code(200) \
        .check_contains("成功")
    
    def test_delete_user_record(self):
        user = User.objects.get(email=RECORD_USER_EMAIL)
        audit_records = AuditRecord.objects.filter(user=user)
        audit_record = audit_records[0]
        wrong_user = User.objects.get(email=USER_EMAIL)
        self.client \
        .with_user_token(wrong_user.email) \
        .do_request(
            "user_delete_audit_record",
            DELETE,
            {
                "audit_record_id": audit_record.id
            }
        ) \
        .check_code(400) \
        .check_contains("无权")
        self.client \
        .with_user_token(user.email) \
        .do_request(
            "user_delete_audit_record",
            DELETE,
            {
                "audit_record_id": audit_record.id
            }
        ) \
        .check_code(200) \
        .check_contains("成功")


