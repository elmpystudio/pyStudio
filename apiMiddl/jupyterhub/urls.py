from django.urls import path, include
from .views import authorizeView, loginView, userView, startView

urlpatterns = [
    path("start/", startView),

    path("authorize/", authorizeView),
    path("token/", loginView),
    path("user/", userView)
]
