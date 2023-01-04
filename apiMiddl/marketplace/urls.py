from django.urls import path
from . import views

urlpatterns = [
    path('datasets', views.DatasetList.as_view()),
    path('ml_models', views.Ml_modelsList.as_view()),
    path('download/<int:pk>', views.DatasetDownload.as_view())
]
