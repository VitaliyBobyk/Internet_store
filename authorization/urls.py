from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]

