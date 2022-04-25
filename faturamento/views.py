import datetime
import functools

from django.http import HttpResponse
from django.template import loader
from faturamento.models import NFE
from faturamento.xml_nfe import LoadXML

# Create your views here.
def faturamento(request):
    nfes = NFE.objects.all().filter(data_emissao__range=[str(datetime.datetime.now().year)+"-01-01", str(datetime.datetime.now().year)+"-12-31"])
    faturamento_ano = calcula_faturamento_anual(nfes)
    if request.method == 'POST':

        print("TESTE")
    anos = range(int(datetime.datetime.now().year)-7,int(datetime.datetime.now().year)+1)
    template = loader.get_template('faturamento.html')
    context = {
        'anos' : anos,
        'nfes' : nfes,
        'faturamento_ano': faturamento_ano,
    }
    return HttpResponse(template.render(context, request))

def calcula_faturamento_anual(nfes):
    soma=0
    for nfe in nfes:
        soma = soma + nfe.servico.valor_servicos
    return soma

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
    if request.method == 'POST':
        xmlfile = request.FILES['arquivoxml']
        nfes = LoadXML(xmlfile).nef_ginfes_maceio()
        # for nfe in nfes:
        #     print(nfe.cliente.endereco)
        #     nfe.servico.save()
        #     nfe.save()

    template = loader.get_template('carregar-xml.html')
    context = {}
    return HttpResponse(template.render(context, request))

def links(request):
    template = loader.get_template('links.html')
    context = {}
    return HttpResponse(template.render(context, request))