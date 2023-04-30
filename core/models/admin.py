from django.db import models

class Admin(models.Model):
    """
    Fields:
        username:
        password:
    """
    username = models.CharField(unique=True, max_length=256)
    password = models.CharField(max_length=256)