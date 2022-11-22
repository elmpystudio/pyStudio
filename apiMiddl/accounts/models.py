from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from utils.minio import minio
# from utils.TableauWrapper import TableauWrapper

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

    roles = models.ManyToManyField(Role, related_name = '+')
    #email = models.CharField(max_length=200, unique=True)
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username'] # removes email from REQUIRED_FIELDS

    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=False, null=True)
    avatar = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=False, null=True)
    creation_ts = models.DateTimeField(default=datetime.now, blank=True, null=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)

    tableau_user = models.CharField(max_length=15, blank=True, null=True)
    tableau_password = models.CharField(max_length=15, blank=True, null=True)

    # JupterHub
    jhub_token = models.TextField(blank=False, null=True)

    class Meta:
        db_table = "user"

    def getAllModels(self, user):
        return minio.getModels(user)

    def get_tableau_trusted_ticket(self):
        return None
        # no longer working as no licencese was paid
        # return TableauWrapper.get_trusted_ticket(self.tableau_user).decode()
        # return TableauWrapper.get_trusted_ticket("api-user").decode()

    def get_tableau_wrapper(self):
        # t = TableauWrapper()
        t = None


    def __str__(self):
        return (
            self.username,
            self.jhub_token
        )

    def get_tableau_project(self):
        t = TableauWrapper()
        proj = t.get_project_by_name(self.email)
        if proj == None:
            proj = t.create_project(self.email, "test descripbion")
        return proj

    def get_tableau_workbooks(self):
        return t.get_workbook_by_project(self.get_tableau_project())

from items.models import Item

class Project(models.Model):

    readonly_fields = ['creation_ts', 'owner']
    owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "+")
    name = models.CharField(max_length=200, blank=False, null=False)
    about = models.TextField(blank=True, null=True)
    collaborators = models.ManyToManyField(CustomUser, related_name = '+')
    creation_ts = models.DateTimeField(default=datetime.now, blank=True, null=True)
    items = models.ManyToManyField(Item, related_name="+")

    def __str__(self):
        return self.name 

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(Project)
