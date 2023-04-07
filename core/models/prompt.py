from django.db import models
from .user import User


LANCHED = 0
UNDER_REVIEW = 1
TAKEN_DOWN = 2
UPLOAD_STATUS_CHOICES = (
    (LANCHED, "LANCHED"),
    (UNDER_REVIEW, "UNDER_REVIEW"),
    (TAKEN_DOWN, "TAKEN_DOWN")
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

    def simple_dict(self):
        data = {
            "id": self.id,
            "prompt": self.prompt,
            "picture": self.picture
        }
        return data

    def full_dict(self):
        data = {
            "id": self.id,
            "prompt": self.prompt,
            "picture": self.picture,
            "model": self.model,
            "width": self.width,
            "height": self.height,
            "created_at": self.created_at,
            "uploader": self.uploader.simple_dict(),
            "upload_status": self.upload_status,
            "prompt_attribute": self.prompt_attribute
        }
        return data

    def review_list_dict(self):
        data = {
            "id": self.id,
            "prompt": self.prompt,
            "picture": self.picture,
            "uploader": self.uploader.mangage_dict(),
            "upload_status": self.upload_status
        }
        return data

    def be_lanched(self):
        self.upload_status = LANCHED
        self.save()
