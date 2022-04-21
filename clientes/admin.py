from django.contrib import admin

# Register your models here.
from clientes.models import Cliente, Endereco

admin.site.register(Cliente)
admin.site.register(Endereco)