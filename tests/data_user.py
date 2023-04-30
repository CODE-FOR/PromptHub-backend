from core.models.user import User
from tests.mock_data_set import DataProvider

USER_EMAIL = "test@test.com"
USER_PASSWORD = "test"
USER_NICKNAME = "test_1"
USER_AVATAR = "user_avatar.jpg"


class UserTestData(DataProvider):
    def set_data(self):
        User.objects.create(
            email=USER_EMAIL,
            password=USER_PASSWORD,
            nickname="test_1",
            is_confirmed=False,
        )

class UserTestDataNotConfirmed(DataProvider):
    def set_data(self):
        User.objects.create(
            email="not_confirmed@test.com",
            password="test_not_confirmed",
            nickname="test_not_confirmed",
            is_confirmed=False,
        )

class UserTestDataGotBanned(DataProvider):
    def set_data(self):
        User.objects.create(
            email="is_banned@test.com",
            password="test_is_banned",
            nickname="test_is_banned",
            is_confirmed=True,
            is_banned=True,
        )
