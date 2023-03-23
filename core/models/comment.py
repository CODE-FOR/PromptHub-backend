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
        is_delete:
    """
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="comment_list")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=4096)
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    
