from tableau import views
from django.urls import include, path

urlpatterns = [
        path('trusted/', views.TableauKeyView.as_view()),
        path('workbooks/', views.TableauWorkbooksView.as_view()),
]
