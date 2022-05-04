from django.contrib import admin

# Register your models here.
from mei.models import Mei, Responsavel, DespesaComprovada

admin.site.register(Mei)
admin.site.register(Responsavel)
admin.site.register(DespesaComprovada)
