from django.urls import path
from . import views

urlpatterns = [
    path("", views.Ml_modelsList.as_view()),
    path("uploadcsv", views.uploadcsv),
    path("run1", views.run1),
    path("run2", views.run2),
    path("<pk>", views.Ml_modelsDetail.as_view()),
]