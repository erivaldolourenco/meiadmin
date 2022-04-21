from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from clientes.models import Cliente


def clientes(request):
    clientes = Cliente.objects.all()
    template = loader.get_template('clientes.html')
    context = {
        'clientes': clientes,
    }
    return HttpResponse(template.render(context, request))