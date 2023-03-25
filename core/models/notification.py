from django.db import models
from .user import User


READ_STATUS_CHOICES = (
    (0, "READ"),
    (1, "UNREAD")
)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    content = models.CharField(max_length=4096)
    status = models.IntegerField(choices=READ_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)