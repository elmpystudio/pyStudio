from django.db import models
from django.contrib.auth import get_user_model
from utils.minio import minio
import uuid

class Dataset(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False,)
    description = models.CharField(max_length=1000, blank=True)
    filename = models.CharField(max_length=200, blank=True, null=False)
    create_at = models.TimeField(auto_now_add=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="+", blank=True)
    file = models.FileField(blank=True)
    is_public = models.BooleanField(default=False)
    purchased = models.ManyToManyField(get_user_model(), related_name="purchased", blank=True)

    bucket = "datasets"

    class Meta:
        db_table = "datasets"

    def __str__(self):
        return "name: %s" % (self.name)

    def download(self, path):
        return minio.download(self.bucket, str(self.uuid), path=path)

    def upload(self, file):
        return minio.put(self.bucket, str(self.uuid), file, file.size)

    def set_science_data_json(self, data):
        return minio.put(self.bucket, str(self.uuid)+"_jsondata", data, len(data))

    def set_science_data_html(self, data):
        return minio.put(self.bucket, str(self.uuid)+"_htmldata", data, len(data))

    def get_science_data_json(self):
        return minio.get(self.bucket, str(self.uuid)+"_jsondata")

    def get_science_data_html(self):
        return minio.get(self.bucket, str(self.uuid)+"_htmldata")

    # def get_science_data(self):
    #     return minio.get(self.bucket, str(self.uuid))

    # def upload_db(self):
    #     sql = build_sql_for_dataset(self.name, self)
    #     exec_in_pg(sql)
