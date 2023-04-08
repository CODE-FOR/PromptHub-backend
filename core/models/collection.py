from django.db import models
from .prompt import Prompt
from .user import User

VISIBILITY_STATUS_CHOICES = (
    (0, "PUBLIC"),
    (1, "PRIVATE")
)


class Collection(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collection_list")
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.IntegerField(choices=VISIBILITY_STATUS_CHOICES)
    cover = models.URLField()

    def full_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "visibility": self.visibility,
            "cover": self.cover,
            "user": self.user.simple_dict()
        }
        return data


class CollectRecord(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="collect_list")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collect_record_list")
    created_at = models.DateTimeField(auto_now_add=True)

    def full_dict(self):
        data = {
            "id": self.id,
            "prompt": self.prompt.simple_dict(),
            "collection": self.collection.id,
        }
        return data