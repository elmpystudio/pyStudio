from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from utils.minio import minio

class Permission(models.Model):
    name = models.CharField(max_length=200)

class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission, related_name = '+')

class Organization(models.Model):
    name = models.CharField(unique=True, max_length=200, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    creation_ts = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=False, null=True)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=False, null=True)
    creation_ts = models.DateTimeField(default=datetime.now, blank=True, null=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)
    jhub_token = models.TextField(blank=False, null=True)
    roles = models.ManyToManyField(Role, related_name = '+')
    tableau_user = models.CharField(max_length=15, blank=True, null=True)
    tableau_password = models.CharField(max_length=15, blank=True, null=True)


    class Meta:
        db_table = "user"

    def getAllModels(self, user):
        return minio.getModels(user)

    def __str__(self):
        return (
            self.username,
            self.jhub_token
        )

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Organization)