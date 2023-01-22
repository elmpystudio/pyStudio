from django.urls import path
from . import views

urlpatterns = [
        path('', views.NotificationList.as_view()),
        # path('<int:pk>', views.NotificationDetail.as_view()),
        path('accept/<int:pk>', views.NotificationAccept.as_view()),
        path('deny/<int:pk>', views.NotificationDeny.as_view()),
    ]
