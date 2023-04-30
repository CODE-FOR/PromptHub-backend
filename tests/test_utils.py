from unittest import TestCase

from django.test.client import Client
from django.urls import reverse

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
    _client = Client()

    status_code = -1
    content = ""
    content_type = "application/json"

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

    def do_request(self, router, method_type, json):
        actual_router = reverse(router)
        response = ""
        if method_type == POST:
            response = self._client.post(actual_router, json, self.content_type)
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
