from django.urls import path
from . import views

urlpatterns = [
    path('', views.MarketplaceList.as_view()),
    path('<int:pk>', views.MarketplaceDetail.as_view()),
    path('download/<int:pk>', views.MarketplaceDownload.as_view())
]
