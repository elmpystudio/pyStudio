from django.urls import path
from django.urls import include, path
from . import views

urlpatterns = [
    # path('', views.User, name='users'),

    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
]
