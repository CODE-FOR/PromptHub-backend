from core.models.collection import Collection, CollectRecord
from core.models.prompt import Prompt
from tests.data_prompt import PromptForCollectionTestData
from tests.data_user import *
from tests.test_utils import *


class CollectionTestCase(TestCase):
    def setUp(self):
        self.data = DataSet(
            UserTestData(),
            PromptForCollectionTestData(),
        )
        self.client = TestClient(self.data)

    def test_create_collection(self):
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_create_collection",
            POST, {
                'name': 'public_collection_1',
                'visibility': 0,
            }
        ).check_contains("成功").check_code(200)

    def test_create_collection_already(self):
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_create_collection",
            POST, {
                'name': 'public_collection_1',
                'visibility': 0,
            }
        ).check_contains("重复的名字").check_code(409)

    def test_delete_collection(self):
        id = Collection.objects.get(name="public_collection_1").id
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_delete_collection",
            POST, {
                'id': id
            }
        ).check_contains("成功").check_code(200)
        pass

    def test_get_collection_info(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        Collection.objects.create(name='test_pub_5', user=user, visibility=0)
        id = Collection.objects.get(name="test_pub_5").id
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_get_collection_info",
            GET, {
                'collection_id': id
            }
        ).check_code(200).check_contains('成功获取')

    def test_add_to_collection(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        collection = Collection.objects.create(name='test_pub_2', user=user,
                                               visibility=0)
        prompt = Prompt.objects.get(prompt='prompt_for_collection')
        # add to collection
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_add_to_collection",
            POST, {
                "collection_id": collection.id,
                "prompt_id": prompt.id
            }
        ).check_code(200).check_contains('成功')

    def test_remove_from_collection(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        collection = Collection.objects.create(name='test_pub_3', user=user,
                                               visibility=0)
        prompt = Prompt.objects.get(prompt='prompt_for_collection')
        id = CollectRecord.objects.create(prompt=prompt,
                                          collection=collection).id
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_remove_from_collection",
            POST, {
                "id": id
            }
        )
        self.assertEquals(
            len(CollectRecord.objects.filter(prompt=prompt,
                                             collection=collection)), 0)

    def test_visibility(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        user2 = User.objects.create(nickname='__sadskajfdlkg',
                                    email="__dgsdgsdg", password='__fafsafdg')
        Collection.objects.create(name='test_private', user=user, visibility=1)
        self.client.with_user_token('__dgsdgsdg').do_request(
            "collection_get_collection_list",
            GET, {
                'fetch_user_id': user.id
            }
        ).check_code(200).check_not_contains('test_private')

        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_get_collection_list",
            GET, {
                'fetch_user_id': user.id
            }
        ).check_code(200).check_contains('test_private')

    def test_modify_collection(self):
        user = User.objects.get(nickname=USER_NICKNAME)
        c = Collection.objects.create(name='test_pub_2', user=user,
                                      visibility=0)
        self.client.with_user_token(USER_EMAIL).do_request(
            "collection_mod_collection",
            PUT, {
                "id": c.id,
                'name': 'abc_def_test_pub_2',
                'visibility': 1
            }
        ).check_contains('成功').check_code(200)
        collection = Collection.objects.get(name='abc_def_test_pub_2')
        self.assertEquals(collection.visibility, 1)
