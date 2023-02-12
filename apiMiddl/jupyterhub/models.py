from django.db import models
from accounts.models import CustomUser

class Jupyter_queue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.TextField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "jupyter_queue"
        
    def __str__(self):
         return "user: %s" % (self.user.id)