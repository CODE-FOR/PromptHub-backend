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
    
    avatar = models.URLField()
    followers = models.ManyToManyField("User")
    is_confirmed = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)