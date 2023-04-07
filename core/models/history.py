from django.db import models
from .user import User
from .prompt import Prompt


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history_list")
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="history_list")
    created_at = models.DateTimeField(auto_now_add=True)

    def simple_dict(self):
        data = {
            "id": self.id,
            "prompt": self.prompt.simple_dict(),
            "created_at": self.created_at
        }
        return data