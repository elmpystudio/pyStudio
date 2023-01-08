from django.urls import path
from . import views

urlpatterns = [
    path("", views.Ml_modelsList.as_view()),
    path("uploadcsv", views.uploadcsv),
    path("run", views.run),
    path("<pk>", views.Ml_modelsDetail.as_view()),
]