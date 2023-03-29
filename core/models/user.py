from django.db import models

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
    
    avatar = models.URLField(default="https://s1.ax1x.com/2023/03/29/ppcWN24.jpg")
    followers = models.ManyToManyField("User")
    is_confirmed = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

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