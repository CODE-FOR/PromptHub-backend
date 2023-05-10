from core.models.notification import COMMENT_NF, UNREAD, READ, Notification
from tests.data_admin import ADMIN_USERNAME, AdminTestData
from tests.data_prompt import *
from tests.data_user import *
from tests.test_utils import *


class NotificationModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(UserTestData(), UserTestTwoData(), AdminTestData())
        self.client = TestClient(self.data)

    # test 评论
    def test_comment_notification(self):
        user = User.objects.get(nickname=USER_NICKNAME2)
        prompt = Prompt.objects.create(
            prompt="prompt_xxgg",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=UNDER_REVIEW,
            prompt_attribute=""
        )

        self.client.with_user_token(USER_EMAIL).do_request(
            'comment_create_comment',
            POST, {"prompt_id": prompt.id, "content": "好看"}
        ).check_contains('成功').check_code(200)

        # 检查通知
        Notification.objects.filter(prompt=prompt)

    # test 通过审核
    def test_system_notification(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        audit_prompt = Prompt.objects.create(
            prompt="test_system_notification",
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
            prompt=audit_prompt,
            status=IN_PROGRESS,
            feedback=""
        )

        audit_record = AuditRecord.objects.filter(prompt=audit_prompt)[0]

        self.client.with_admin_token(ADMIN_USERNAME).do_request(
            "admin_audit_prompt",
            POST, {"id": audit_record.id, "passed": True, "content": ""}
        ).check_contains("完成").check_code(200)
        # 检查
        Notification.objects.filter(prompt=audit_prompt)

    def test_get_notification_list(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        prompt = Prompt.objects.create(
            prompt="prompt_get_notif_list",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=UNDER_REVIEW,
            prompt_attribute=""
        )
        notif = Notification.objects.create(
            user=user, prompt=prompt, title='Test get notif list', content='None', status=UNREAD, nf_type=COMMENT_NF)

        self.client.with_user_token(USER_EMAIL).do_request(
            'notification_get_notification_list',
            GET,
            {
                'nf_type': UNREAD
            }
        ).check_code(200).check_contains("notif list")

    def test_delete_notifcation(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        prompt = Prompt.objects.create(
            prompt="notif_delete",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=UNDER_REVIEW,
            prompt_attribute=""
        )
        notif = Notification.objects.create(
            user=user, prompt=prompt, title='notif_delete', content='None', status=UNREAD, nf_type=COMMENT_NF)

        self.client.with_user_token(USER_EMAIL).do_request(
            'notification_delete_notification',
            DELETE,
            {
                'id': notif.id
            }
        ).check_code(200).check_not_contains("notif_delete")

    def test_get_num(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        prompt = Prompt.objects.create(
            prompt="prompt_get_notif_list",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=UNDER_REVIEW,
            prompt_attribute=""
        )
        notif = Notification.objects.create(
            user=user, prompt=prompt, title='unread num for 1', content='None', status=UNREAD, nf_type=COMMENT_NF)
        self.client.with_user_token(USER_EMAIL).do_request(
            "notification_get_unread_notification_num",
            GET,
            {

            }
        ).check_code(200).check_contains('unread_notification_num\": 1')

    def test_update_notif(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        prompt = Prompt.objects.create(
            prompt="prompt_get_notif_list",
            picture="picture.jpg",
            model="model",
            width=512,
            height=512,
            uploader=user,
            upload_status=UNDER_REVIEW,
            prompt_attribute=""
        )
        notif = Notification.objects.create(
            user=user, prompt=prompt, title='to update', content='None', status=UNREAD, nf_type=COMMENT_NF)
        self.client.with_user_token(USER_EMAIL).do_request(
            'notification_update_notification',
            POST,
            {
                'id': notif.id,
                'status': READ
            }
        ).check_code(200).check_contains("成功")
