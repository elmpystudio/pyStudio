from django.contrib import admin
from .models import *

class DatasetAdmin(admin.ModelAdmin):
    exclude = ("item",)

class ItemAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
       return False

# admin.site.register(Dataset, DatasetAdmin)
# #admin.site.register(Item, ItemAdmin)

# admin.site.register(Asset)
# admin.site.register(VisualAnalytics)
