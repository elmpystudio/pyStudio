from django.urls import path
from .views import *

urlpatterns = [
    path('offering/', OfferingView.as_view(), name='offering'),
    path('purchase/', PurchaseView.as_view(), name='purchase')
]
