from unittest import TestCase

from django.urls import reverse
from rest_framework.test import APIClient

from core.api.auth import generate_access_token, generate_refresh_token, \
    ACCOUNT_TYPE_USER, ACCOUNT_TYPE_ADMIN
from core.models.admin import Admin
from core.models.user import User
from tests.mock_data_set import DataSet

POST = 0
GET = 1
DELETE = 2
PUT = 3

HTTP_METHOD = (
    (POST, "POST"),
    (GET, "GET"),
    (DELETE, "DELETE"),
    (PUT, "PUT")
)


class TestClient:
    _client = APIClient()

    status_code = -1
    content = ""
    content_type = "json"
    token = ""
    enable_token = False

    def __init__(self, data):
        if data is None:
            return
        if not isinstance(data, DataSet):
            raise TypeError(
                "required type: DataProvider, given type: " + type(data))
        data.set_data()

    def check_code(self, code):
        TestCase().assertEquals(self.status_code, code)
        return self

    def check_contains(self, str_should_contain):
        success = str_should_contain in self.content
        if not success:
            print(str_should_contain + "\n NOT IN\n" + self.content)
        TestCase().assertTrue(success)
        return self

    def check_not_contains(self, str_should_contain):
        success = str_should_contain in self.content
        if success:
            print(str_should_contain + "\n IN\n" + self.content)
        TestCase().assertFalse(success)
        return self

    def check_true(self, bool_var):
        TestCase().assertTrue(bool_var)

    def check_false(self, bool_var):
        TestCase().assertFalse(bool_var)

    def do_request(self, router, method_type, json):
        if self.enable_token:
            self._client.credentials(
                HTTP_AUTHORIZATION='Bearer ' + self.token)
        actual_router = reverse(router)
        response = ""
        if method_type == POST:
            response = self._client.post(
                actual_router, json, self.content_type)
        if method_type == GET:
            response = self._client.get(actual_router, json)
        if method_type == DELETE:
            response = self._client.delete(actual_router, json,
                                           self.content_type)
        if method_type == PUT:
            response = self._client.put(actual_router, json, self.content_type)
        self.status_code = response.status_code
        self.content = response.content.decode('unicode-escape')
        TestCase().assertNotEquals(response, "")
        return self

    def with_user_token(self, email):
        self.enable_token = True
        user = User.objects.get(email=email)
        if user is None:
            TestCase().fail("internal error -> can not obtain token")
        self.token = generate_access_token(user.id, ACCOUNT_TYPE_USER)
        return self

    def get_user_id(self, name):
        user = User.objects.get(nickname=name)
        if user is None:
            TestCase().fail("internal error -> can not obtain token")
        return user.id

    def with_admin_token(self, username):
        self.enable_token = True
        admin = Admin.objects.get(username=username)
        if admin is None:
            TestCase().fail("internal error -> can not obtain token")
        self.token = generate_access_token(admin.id, ACCOUNT_TYPE_ADMIN)
        return self

    def with_admin_refresh_token(self, username):
        self.enable_token = True
        admin = Admin.objects.get(username=username)
        if admin is None:
            TestCase().fail("internal error -> can not obtain token")
        self.token = generate_refresh_token(admin.id, ACCOUNT_TYPE_ADMIN)
        return self
