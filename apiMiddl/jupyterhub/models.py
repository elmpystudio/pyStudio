from django.db import models
from accounts.models import CustomUser
from datetime import datetime

class Jupyter(models.Model):
    client_id = models.TextField(blank=False, null=False)
    is_open = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "Jupyter"
        
    def __str__(self):
        return (
            self.client_id,
            self.is_open
        )

class Jupyter_history(models.Model):
    create_at = models.DateTimeField(default=datetime.now, blank=False, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "Jupyter_history"
        
    def __str__(self):
        return (
            self.create_at,
            self.user
        )