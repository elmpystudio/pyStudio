from django.urls import path
from . import views

urlpatterns = [
    path("", views.service_list),
    path("<pk>", views.service_detail),
    path("run", views.run),
    path("uploadcsv", views.uploadcsv),
    path("<pk>", views.service_detail)
]