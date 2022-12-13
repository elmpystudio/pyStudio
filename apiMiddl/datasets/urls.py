from django.urls import path
from . import views

urlpatterns = [
        path('', views.DatasetList.as_view()),
        path('<int:pk>', views.DatasetDetail.as_view()),
        path('sample/<int:pk>', views.DatasetSampleView.as_view()),
        path('raport/html/<int:pk>', views.DatasetRaportHtmlView.as_view()),
        path('raport/json/<int:pk>', views.DatasetRaportJsonView.as_view()),
    ]
