from locust import HttpUser, task, between, run_single_user

class Tests(HttpUser):
    wait_time = between(2, 5)
    host = "http://47.93.21.142:8080"

    def on_start(self):
        email = "liuzhenweilzw@163.com"
        password = "345"
        self.client.post(
            "/api/auth/user_obtain_token",
            json={
                "email": email,
                "password": password
            }
        )
    
    @task
    def user_api(self):
        self.client.get("/api/user/get_user_simple_dict?id=1")
        self.client.get("/api/user/get_user_following_num?user_id=2")
        self.client.get("/api/user/get_user_following_list?user_id=2")
        self.client.get("/api/user/get_user_follower_num?user_id=2")
        self.client.get("/api/user/get_user_follower_list?user_id=2")
        self.client.get("/api/user/get_published_prompt_num?user_id=2")
        self.client.get("/api/user/get_published_prompt_list?user_id=2")
    
    @task
    def prompt_api(self):
        self.client.get("/api/prompt/get_prompt?id=591")
        self.client.get("/api/prompt_list/hot_prompt_list")
        self.client.get("/api/prompt_list/search_prompt_keyword?keyword=fish")

    @task
    def comment_and_collection_api(self):
        self.client.get("/api/comment/get_comment_list?prompt_id=2")
        self.client.get("/api/collection/get_collection_list?fetch_user_id=2")

    @task
    def prompt_personalized_api(self):
        self.client.get("/api/prompt_list/personized_prompt_list")