from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
import xml.etree.ElementTree as ET

from faturamento.models import NFE
from faturamento.xml_nfe import LoadXML


def home(request):
    template = loader.get_template('index.html')
    context = {
        'teste': 'teste',
    }
    return HttpResponse(template.render(context, request))


def inf_nfe_ano(request):
    anos = ['2015', '2016', '2017', '2018', '2019', '2020', '2021','2022']
    lista = []
    for ano in anos:
        nfes = NFE.objects.all().filter(data_emissao__range=[ano + "-01-01", ano + "-12-31"])
        soma = 0
        for nfe in nfes:
            soma += nfe.servico.valor_servicos
        lista.append(
            {
                "ano": ano,
                "valor": soma
            }
        )
    template = loader.get_template('inf-nfe-ano.html')
    context = {
        'nfes': lista,
    }
    return HttpResponse(template.render(context, request))


def carregar_xml(request):
    xmlfile = request.FILES['arquivoxml']

    nfes = LoadXML(xmlfile).nef_ginfes_maceio()
    for nfe in nfes:
        print(nfe.tomador.endereco)
        nfe.tomador.endereco.save()
        nfe.tomador.save()
        nfe.servico.save()
        nfe.save()

    template = loader.get_template('carregar-xml.html')
    context = {
        'xml': nfes,
    }
    return HttpResponse(template.render(context, request))
