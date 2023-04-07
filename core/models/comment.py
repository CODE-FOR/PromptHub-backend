from django.db import models
from .prompt import Prompt
from .user import User

class Comment(models.Model):
    """
    Fields:
        prompt: a foreignkey to prompt
        user: a foreignkey to user
        created_at:
        content:
        parent_comment:
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="comment_list")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=4096)
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    
    def simple_dict(self, **kwargs):
        data = {
            "id": self.id,
            "user": self.user.simple_dict(),
            "created_at": self.created_at,
            "content": self.content,
            "prompt_id": self.prompt.id
        }

        user_id = kwargs.get("user_id", None)
        if user_id:
            data["belong_to"] = user_id == self.user.id
        return data
    
    def full_dict(self, **kwargs):
        data = self.simple_dict(**kwargs)
        if self.parent_comment:
            data["parent_comment"] = self.parent_comment.simple_dict()
        return data
