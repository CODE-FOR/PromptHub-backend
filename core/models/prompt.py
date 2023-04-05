from django.db import models
from .user import User


UPLOAD_STATUS_CHOICES = (
    (0, "LANCHED"),
    (1, "UNDER_REVIEW"),
    (2, "TAKEN_DOWN")
)


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
    created_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompts")
    upload_status = models.IntegerField(choices=UPLOAD_STATUS_CHOICES)
    prompt_attribute = models.CharField(max_length=4096)
    is_delete = models.BooleanField(default=False)


