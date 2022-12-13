from django.db import models

class Service(models.Model):
    name = models.TextField(blank=False, null=True)
    model_name = models.TextField(blank=False, null=True)
    username = models.TextField(blank=False, null=True)
    description = models.TextField(blank=False, null=True)
    version = models.FloatField(blank=False, null=True)
    eval_metrics = models.TextField(blank=False, null=True)
    columns = models.TextField(blank=False, null=True)

    class Meta:
        db_table = "services"
        
    def __str__(self):
        return self.name