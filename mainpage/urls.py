from django.urls import path, include
from .views import *
from . import views


urlpatterns = [
    path('', ItemsView.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('shop/', Shop.as_view(), name='shop_product'),
    path('shop/search', Shop.as_view(), name='shop'),
    path('product_detail/<int:pk>/', ProductDetail.as_view(), name='product'),
]