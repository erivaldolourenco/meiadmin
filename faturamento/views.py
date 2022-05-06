import datetime
from decimal import Decimal
from functools import reduce
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from faturamento.models import NFE
from faturamento.xml_nfe import LoadXML
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
from mei.models import DespesaComprovada


@login_required
def faturamento(request, ano=datetime.now().year):
    nfes = NFE.objects.all().filter(mei=request.user.responsavel.mei)
    despesas = DespesaComprovada.objects.all().filter(mei=request.user.responsavel.mei)
    anos = sorted(list(set(map(lambda nfe: nfe.data_emissao.year, nfes))))
    faturamento_ano = reduce(
        lambda total, nfe: total + nfe.servico.valor_servicos,
        filter(lambda nfe: nfe.data_emissao.year == int(ano), nfes),
        Decimal(0)
    )
    despesas_comprovadas_ano = reduce(
        lambda total, despesa: total + despesa.valor,
        filter(lambda despesa: despesa.upload_date.year == int(ano), despesas),
        Decimal(0)
    )
    redimento_isento = round(faturamento_ano * 32 / 100, 2)
    redimento_tributavel = round(faturamento_ano - redimento_isento,2)
    lucro = round(redimento_tributavel - Decimal(despesas_comprovadas_ano),2)

    template = loader.get_template('faturamento.html')
    context = {
        'ano' : ano,
        'anos' : anos,
        'lucro' : lucro,
        'despesas_comprovadas': despesas_comprovadas_ano,
        'redimento_tributavel' : redimento_tributavel,
        'redimento_isento' : redimento_isento,
        'faturamento_ano': round(faturamento_ano,2),
    }
    return HttpResponse(template.render(context, request))


@login_required
def inf_nfe_ano(request):
    nfes = NFE.objects.all().filter(mei = request.user.responsavel.mei)
    anos = sorted(list(set(map(lambda nfe: nfe.data_emissao.year, nfes))))
    faturamento_anos = []
    for ano in anos:
        valor_ano =  reduce(
            lambda total, nfe: total + nfe.servico.valor_servicos,
            filter(lambda nfe: nfe.data_emissao.year == ano, nfes),
            Decimal(0)
        )
        faturamento_anos.append({"ano": ano,"valor": valor_ano})
    template = loader.get_template('inf-nfe-ano.html')
    context = {
        'faturamento_anos': faturamento_anos,
    }
    return HttpResponse(template.render(context, request))

@login_required
def carregar_xml(request):
    if request.method == 'POST':
        xmlfiles = request.FILES.getlist('arquivoxml')
        nfes=[]
        for xmlfile in xmlfiles:
            nfes.append(LoadXML(xmlfile, request).obter_nfes())
        messages.add_message(
            request, messages.SUCCESS,
            'Foram adicionadas ' + str(nfes.__sizeof__()) + ' NFEs!',
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
    nfes = NFE.objects.all().filter(mei = request.user.responsavel.mei)
    template = loader.get_template('nfes.html')
    context = {'nfes':nfes}
    return HttpResponse(template.render(context, request))