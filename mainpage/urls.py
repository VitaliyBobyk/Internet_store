from django.urls import path
from .views import *


urlpatterns = [
    path('', ItemsView.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('shop/', Shop.as_view(), name='shop_product'),
    path('shop/search', Shop.as_view(), name='shop'),
    path('product_detail/<int:pk>/', ProductDetail.as_view(), name='product'),
    path('shop/product_detail/<int:pk>/', ProductDetail.as_view(), name='product'),
    path('shop_list/', Shop.as_view(), name='shop_list'),
    path('shop_list/search', Shop.as_view(), name='shop_list_search'),
    path('shop_list/product_detail/<int:pk>/', ProductDetail.as_view(), name='product'),
]
