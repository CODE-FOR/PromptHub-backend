from django.db import models
from .prompt import Prompt
from .user import User

AUDIT_STATUS_CHOICES = (
    (0, "PASSED"),
    (1, "REJECTED"),
    (2, "IN_PROGRESS")
)

class AuditRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audit_record_list")
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="audit_record_list")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=AUDIT_STATUS_CHOICES)
    feedback = models.CharField(max_length=4096)