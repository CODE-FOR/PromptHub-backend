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

class CollectRecord(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="collect_list")
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collect_record_list")
    created_at = models.DateTimeField(auto_now_add=True)

