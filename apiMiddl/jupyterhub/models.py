from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Jupyter_queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "jupyter_queue"
        
    def __str__(self):
         return "user: %s" % (self.user.id)