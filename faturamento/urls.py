from django.contrib import admin
from django.urls import path, include

from faturamento import views

urlpatterns = [
    path('', views.faturamento, name='faturamento'),
    path('<ano>', views.faturamento, name='faturamento'),
    path('carregar-xml', views.carregar_xml, name='carregar_xml'),
    path('inf-nfe-ano', views.inf_nfe_ano, name='inf_nfe_ano'),
    path('nfes', views.nfes, name='nfes'),
]