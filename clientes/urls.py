from django.contrib import admin
from django.urls import path, include

from clientes import views

urlpatterns = [
    path('', views.clientes, name='clientes'),
]