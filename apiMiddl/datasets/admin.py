from django.contrib import admin
from .models import *

class DatasetAdmin(admin.ModelAdmin):
    exclude = ("dataset",)

class DatasetAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
       return False
