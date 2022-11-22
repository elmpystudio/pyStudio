from django.db import models

from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()


class MlWorkflow(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    creation_ts = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_save = models.DateTimeField(default=datetime.now, blank=True, null=True)
    wf_json = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.title) + str(self.user.username) + + str(self.wf_json)

    class Meta:
        db_table = 'ml_workflow'

