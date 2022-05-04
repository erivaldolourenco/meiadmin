from django.contrib import admin

# Register your models here.
from faturamento.models import Servico, NFE

admin.site.register(Servico)
admin.site.register(NFE)