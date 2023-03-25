from django.db import models
from .prompt import Prompt


class Tag(models.Model):
    tag = models.CharField(max_length=256)
    prompt = models.ManyToManyField(to=Prompt, related_name="tag_list")