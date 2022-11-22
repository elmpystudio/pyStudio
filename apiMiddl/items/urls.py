from django.urls import path, include
from rest_framework.routers import DefaultRouter
from items import views

# Create a router and register our viewsets with it.
"""
router = DefaultRouter()
router.register(r'datasets', views.DatasetAPI.as_view(), basename="Datasets")
urlpatterns = router.urls
"""
urlpatterns = [
        path('file_upload/<filename>/', views.FileUploadView.as_view()),
        path('datasets/', views.DatasetListCreateView.as_view()),
        path('datasets/<id>', views.DatasetUpdateView.as_view()),
        path('sample/<dataset_id>/', views.DatasetSampleView.as_view()),
        path('raport/html/<dataset_id>/', views.DatasetRaportHtmlView.as_view()),
        path('raport/json/<dataset_id>/', views.DatasetRaportJsonView.as_view()),
        path('va/', views.VisualAnalyticsView.as_view()),
        path('dashboard/<items_type>/', views.DashboardView.as_view())
    ]
