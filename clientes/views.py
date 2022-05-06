from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader

from clientes.models import Cliente
# Create your views here.


@login_required
def clientes(request):
    clientes = Cliente.objects.all().filter(mei = request.user.responsavel.mei)
    template = loader.get_template('clientes.html')
    context = {
        'clientes': clientes,
    }
    return HttpResponse(template.render(context, request))