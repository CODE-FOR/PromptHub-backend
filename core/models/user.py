from django.db import models
import random

def get_default_avatar():
    default_avatars = [
        "https://image.lexica.art/full_jpg/d79768c4-fe89-4099-874d-87b7a77ecc24",
        "https://image.lexica.art/full_jpg/314c275a-2108-4766-9b34-a33396e3402a",
        "https://image.lexica.art/full_jpg/73b59d28-2383-4537-b263-3f9177c60a86",
        "https://image.lexica.art/full_jpg/d7256b0f-5901-4792-a2f6-f4d01051c849",
        "https://image.lexica.art/full_jpg/2d45709c-30c9-43ee-95da-e99785b887bb",
        "https://image.lexica.art/full_jpg/287d0cef-2af6-4a2c-a9d9-7d9843719f72",
        "https://image.lexica.art/full_jpg/d4cd3ce3-8ef9-453d-80e4-779943b67b77",
        "https://image.lexica.art/full_jpg/2c6e89b4-3e57-423f-8336-28c01610ac43",
        "https://image.lexica.art/full_jpg/d07e6bc9-8aab-40d5-b0eb-a8de91dc632b",
        "https://image.lexica.art/full_jpg/8b164e89-c29e-4182-901c-22f888d1ccbb",
    ]
    return default_avatars[random.randint(0, len(default_avatars) - 1)]

class User(models.Model):
    """
    Fields:
        username:
        password:
        email:
        avatar:
        followers:
        is_confirmed: whether email is confirmed
        is_banned:
    """
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    nickname = models.CharField(max_length=256)

    avatar = models.URLField(default=get_default_avatar())
    is_confirmed = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    def simple_dict(self):
        data = {
            "id": self.id,
            "nickname": self.nickname,
            "avatar": self.avatar
        }
        return data

    def manage_dict(self):
        data = {
            "id": self.id,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "is_banned": self.is_banned
        }
        return data

    def check_password(self, password):
        return self.password == password

class ConfirmCode(models.Model):
    """confirm code
    Field
        email:
        code: check code
    """
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=5)
    expire_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')} {self.email}: {self.code}"

class UserFollowing(models.Model):
    user = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey("User", related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)