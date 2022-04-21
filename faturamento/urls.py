from django.contrib import admin
from django.urls import path, include

from faturamento import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carregar-xml', views.carregar_xml, name='carregar_xml'),
    path('inf-nfe-ano', views.inf_nfe_ano, name='inf_nfe_ano'),
]