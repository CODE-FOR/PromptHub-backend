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
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    email = models.EmailField()
    avatar = models.URLField()
    followers = models.ManyToManyField("User")
    is_confirmed = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)