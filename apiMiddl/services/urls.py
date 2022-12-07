from django.urls import path
from . import views

urlpatterns = [
    path("", views.service_list),
    path("run", views.run),
    path("uploadcsv", views.uploadcsv),
    path("<pk>", views.service_detail)
]