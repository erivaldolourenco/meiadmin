from django.contrib import admin

# Register your models here.
from faturamento.models import Servico, NFE, DespesaComprovada

admin.site.register(Servico)
admin.site.register(NFE)
admin.site.register(DespesaComprovada)