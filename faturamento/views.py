import datetime
from decimal import Decimal
import functools
from unicodedata import decimal
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from faturamento.models import NFE
from faturamento.xml_nfe import LoadXML
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def faturamento(request):
   
    if request.method == 'POST':
        ano  = request.POST['ano']
        despesas = request.POST['despesas']
        nfes = NFE.objects.all().filter(data_emissao__range=[str(ano)+"-01-01", str(ano)+"-12-31"])
        faturamento_ano = calcula_faturamento_anual(nfes)
        redimento_isento = faturamento_ano*32/100
        redimento_tributavel = faturamento_ano - redimento_isento
        lucro =  redimento_tributavel - Decimal(despesas)
    else:
        despesas = 0
        ano = datetime.datetime.now().year
        nfes = NFE.objects.all().filter(data_emissao__range=[str(ano)+"-01-01", str(ano)+"-12-31"])
        faturamento_ano = calcula_faturamento_anual(nfes)
        redimento_isento = faturamento_ano*32/100
        redimento_tributavel = faturamento_ano - redimento_isento
        lucro =  Decimal(redimento_tributavel) - Decimal(despesas)


    messages.add_message(
        request, messages.SUCCESS, 
        'Bem-vindo ',
        fail_silently=True,
            )
    template = loader.get_template('faturamento.html')
    context = {
        'lucro' : lucro,
        'redimento_tributavel' : redimento_tributavel,
        'redimento_isento' : redimento_isento,
        'ano' : ano,
        'anos' : range(int(datetime.datetime.now().year)-7,int(datetime.datetime.now().year)+1),
        'nfes' : nfes,
        'faturamento_ano': faturamento_ano,
    }
    return HttpResponse(template.render(context, request))

def calcula_faturamento_anual(nfes):
    soma=0
    for nfe in nfes:
        soma = soma + nfe.servico.valor_servicos
    return soma

@login_required
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

@login_required
def carregar_xml(request):
    if request.method == 'POST':
        xmlfiles = request.FILES.getlist('arquivoxml')
        nfes=[]
        for xmlfile in xmlfiles:      
            nfes.append(LoadXML(xmlfile).obter_nfes())

        messages.add_message(
        request, messages.SUCCESS, 
        'Nfes adicionada ao banco '+str(nfes),
        fail_silently=True,
            )

    template = loader.get_template('carregar-xml.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def links(request):
    template = loader.get_template('links.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def nfes(request):
    nfes = NFE.objects.all()
    template = loader.get_template('nfes.html')
    context = {'nfes':nfes}
    return HttpResponse(template.render(context, request))