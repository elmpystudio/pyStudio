from django.urls import path
from django.urls import include, path
from accounts.views.signup import *

urlpatterns = [
    path("accounts/", include([
        path('users/', UserView.as_view())]
    )),
    path('login/', LoginView.as_view(), name='login'),
    path('ses/', log, name='ses'),
    path('register/', RegisterView.as_view(), name='register')
]
