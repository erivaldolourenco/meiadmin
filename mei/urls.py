from django.contrib import admin
from django.urls import path, include

from mei import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('logout', views.logout, name='logout'),
    path('mei', views.mei, name='mei'),
    path('despesas', views.despesas_comprovadas, name='despesas_comprovadas'),
]