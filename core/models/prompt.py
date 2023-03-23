from django.db import models
from .user import User

class Prompt(models.Model):
    """
    prompt:
    picture:
    model:
    width:
    height:
    uploader:
    """
    prompt = models.CharField(max_length=4096)
    picture = models.URLField()
    model = models.CharField(max_length=256)
    width = models.IntegerField()
    height = models.IntegerField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompts")

