from django.urls import path, include
from . import views

urlpatterns = [
    path("open", views.open),
    path("sync", views.sync),

    # for Jupyterhub only
    path("auth_step1/", views.auth_step1),
    path("auth_step2/", views.auth_step2),
    path("auth_step3/", views.auth_step3)
]
