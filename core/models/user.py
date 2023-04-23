from django.db import models
import random

def get_default_avatar():
    default_avatars = [
        "https://s1.ax1x.com/2023/04/23/p9e3H5d.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e3vKf.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e37UH.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e3IbD.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e3TVe.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e3O2t.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e3L8I.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e8pVg.jpg",
        "https://s1.ax1x.com/2023/04/23/p9e3zqS.jpg",
        "https://s1.ax1x.com/2023/03/29/ppcWN24.jpg",
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