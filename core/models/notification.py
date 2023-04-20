from django.db import models
from .user import User
from .prompt import Prompt

READ = 0
UNREAD = 1
READ_STATUS_CHOICES = (
    (0, "READ"),
    (1, "UNREAD")
)

SYSTEM_NF = 0
COMMENT_NF = 1

NOTIFICATION_TYPE_CHOICES = (
    (SYSTEM_NF, "SYSTEM_NF"),
    (COMMENT_NF, "COMMENT_NF")
)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="related_notifications")
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=4096)
    status = models.IntegerField(choices=READ_STATUS_CHOICES)
    nf_type = models.IntegerField(choices=NOTIFICATION_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def simple_dict(self):
        data = {
            "notification_id": self.id,
            "prompt_id": self.prompt.id,
            "prompt_upload_status": self.prompt.upload_status,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at
        }
        return data