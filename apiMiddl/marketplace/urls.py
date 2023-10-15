from django.urls import path
from . import views

urlpatterns = [
    path('datasets', views.DatasetList.as_view()),
    path('ml_models', views.Ml_modelsList.as_view()),
    path('datasets/download/<int:pk>', views.DatasetDownload.as_view()),
    path('ml_models/download/<int:pk>', views.Ml_modelDownload.as_view()),
    path('datasets/add/<int:pk>', views.DatasetAdd.as_view()),
    path('ml_models/add/<int:pk>', views.Ml_modelAdd.as_view())
]
