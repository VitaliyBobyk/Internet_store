from django.urls import path
from .views import *

urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
]
