from core.models.admin import Admin
from tests.mock_data_set import DataProvider

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"


class AdminTestData(DataProvider):
    def set_data(self):
        Admin.objects.create(
            username=ADMIN_USERNAME,
            password=ADMIN_PASSWORD,
        )
