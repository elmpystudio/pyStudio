from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser as User
from datasets.models import Dataset

class Notification(models.Model):
    message = models.CharField(max_length=255, null=False, blank=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user", blank=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user", blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="dataset", blank=True, null=True)
    # ml_model = models.ForeignKey(Ml_model, on_delete=models.CASCADE, related_name="ml_model", blank=True, null=True)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return "message: %s" % (self.message)


