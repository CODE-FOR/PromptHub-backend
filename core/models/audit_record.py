from django.db import models
from .prompt import Prompt
from .user import User

PASSED = 0
REJECTED = 1
IN_PROGRESS = 2
AUDIT_STATUS_CHOICES = (
    (PASSED, "PASSED"),
    (REJECTED, "REJECTED"),
    (IN_PROGRESS, "IN_PROGRESS")
)

class AuditRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audit_record_list")
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="audit_record_list")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=AUDIT_STATUS_CHOICES)
    feedback = models.CharField(max_length=4096)
    is_delete = models.BooleanField(default=False)

    def to_dict(self):
        data = {
            "audit_record_id": self.id,
            "user": self.user.simple_dict(),
            "prompt": self.prompt.simple_dict(),
            "created_at": self.created_at,
            "status": self.status,
            "feedback": self.feedback
        }
        return data

    def be_deleted(self):
        self.is_delete = True
        self.save()

    def be_passed(self):
        self.status = PASSED
        self.save()

    def be_rejected(self):
        self.status = REJECTED
        self.save()