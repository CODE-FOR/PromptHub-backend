from tests.test_utils import *
from tests.data_prompts import *


class PromptsModelTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(PromptListTestData())
        self.client = TestClient(self.data)
    
    def test_prompt_list_search_prompt_keyword(self):
        keyword = "2"
        self.client \
        .do_request(
            "prompt_list_search_prompt_keyword",
            GET,
            {
                "keyword": keyword,
            }
        ) \
        .check_code(200) \
        .check_contains("成功")

    def test_prompt_list_hot_prompt_list(self):
        self.client \
        .do_request(
            "prompt_list_hot_prompt_list",
            GET,
            {}
        ) \
        .check_code(200) \
        .check_contains("成功")

    def test_prompt_list_personalized_prompt_list(self):
        # random
        self.client \
        .do_request(
            "prompt_list_personalized_prompt_list",
            GET,
            {}
        ) \
        .check_code(200) \
        .check_contains("成功")