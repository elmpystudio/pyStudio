from django.db import models
from django.db.models.signals import post_init, pre_init
from django.contrib import admin
from django.contrib.auth import get_user_model
from utils.minio import minio
from utils.random_utils import *
import uuid
import pickle as pkl

User = get_user_model()

class Item(models.Model):

    private = models.ManyToManyField(User, related_name="private")
    purchased = models.ManyToManyField(User, related_name="purchased")

    def get_item(self):
        if hasattr(self, "dataset_relation"):
            return self.dataset_relation
        if hasattr(self, "va_relation"):
            return self.va_relation
        if hasattr(self, "asset_relation"):
            return self.dataset_relation

    class Meta:
        db_table = "items"
        
    def __str__(self):
        return str(self.get_item())

class File(models.Model):

    filename = models.CharField(max_length=200, blank=False, null=False)
    uploadDate = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "+")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        db_table = "file"

    def __str__(self):
        return "filename: %s uuid: %s uploaded: %s" % (self.filename, str(self.uuid), self.uploadDate)

    def download(self, bucket, path):
        return minio.download(bucket, str(self.uuid), path=path)

    def get(self, bucket):
        return minio.get(bucket, str(self.uuid))

    def save_to_minio(self, bucket, data, data_len):
        return minio.put(bucket, str(self.uuid), data, data_len)


class Dataset(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)

    id = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name = "dataset_relation",
        primary_key = True
    )

    bucket = "datasets"

    def save(self, *args, **kwargs):
        set_item_as_id_if_empty(self)
        super(Dataset, self).save(*args, **kwargs)

    class Meta:
        db_table = "datasets"

    def get_content(self):
        return self.file.get(self.bucket)

    def set_science_data_json(self, data):
        return minio.put(self.bucket, str(self.file.uuid)+"_jsondata", data, len(data))

    def set_science_data_html(self, data):
        return minio.put(self.bucket, str(self.file.uuid)+"_htmldata", data, len(data))

    def get_science_data_json(self):
        return minio.get(self.bucket, str(self.file.uuid)+"_jsondata")

    def get_science_data(self):
        return minio.get(self.bucket, str(self.file.uuid))

    def get_science_data_html(self):
        return minio.get(self.bucket, str(self.file.uuid)+"_htmldata")

    def download(self, path):
        return minio.download(self.bucket, str(self.file.uuid), path=path)

    def download_models(model_name, path):
        return minio.download('deployed-objects', model_name, path)

    def __str__(self):
        return "name: %s" % (self.name)

    def upload_db(self):
        sql = build_sql_for_dataset(self.name, self)
        exec_in_pg(sql)

    @property
    def display_type_name(self):
        return "Dataset"


class VisualAnalytics(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    tableau_workbook_id = models.CharField(max_length=200, blank=False, null=False)

    id = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name = "va_relation",
        primary_key = True
    )

    @property
    def display_type_name(self):
        return "Visual Analitycs"

    def save(self, *args, **kwargs):
        set_item_as_id_if_empty(self)
        super(VisualAnalytics, self).save(*args, **kwargs)

    class Meta:
        db_table = "visualanalytic"

class Asset(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    id = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name = "asset_relation",
        primary_key = True
    )

    def save(self, *args, **kwargs):
        set_item_as_id_if_empty(self)
        super(Asset, self).save(*args, **kwargs)

    class Meta:
        db_table = "assets"

def set_item_as_id_if_empty(o):
    if not hasattr(o, "id"):
        o.id = Item.objects.create()


"""
class Report(Item):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(Asset, related_name = '+')

    class Meta:
        db_table = "report"

class ItemReference(models.Model):


"""

"""
from django.dispatch import receiver
from django.db.models.signals import pre_save

@receiver(pre_save, sender=Dataset)
@receiver(pre_save, sender=Asset)
@receiver(pre_save, sender=VisualAnalytics)
def add_item_as_id(sender, instance, *args, **kwargs):

    if instance.id == None:
        print("--------------")
        print("NIe ma id, jest ok")
        print("--------------")
    return
"""
