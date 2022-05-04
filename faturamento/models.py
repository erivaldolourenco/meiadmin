from django.db import models
from clientes.models import Cliente
import datetime
import os
# Create your models here.


def path_file_media(instance, filename):
    date = datetime.date.today()
    path = 'upload/' + str(date.year) + '/' + str(date.month)
    file_name = '{0}'.format(filename.lower().replace(' ','-'))
    return os.path.join(path, file_name)

class Servico(models.Model):
    valor_servicos = models.DecimalField(max_digits=6,decimal_places=2)
    iss_retido = models.DecimalField(max_digits=6,decimal_places=2)
    valor_iss = models.DecimalField(max_digits=6,decimal_places=2)
    base_calculo = models.DecimalField(max_digits=6,decimal_places=2)
    aliquota = models.DecimalField(max_digits=6,decimal_places=2)
    valor_liquido_nfse = models.DecimalField(max_digits=6,decimal_places=2)
    valor_iss_retido = models.DecimalField(max_digits=6,decimal_places=2)
    item_lista_servico = models.CharField(max_length=50)
    codigo_tributacao_municipio = models.CharField(max_length=50)
    descricao = models.TextField(max_length=500, blank=True)
    municipio_prestacao_servico = models.CharField(max_length=50)

    def __str__(self):
        return str(self.descricao)+"-"+str(self.valor_servicos)

class NFE(models.Model):
    numero = models.IntegerField()
    codigo_verificacao = models.CharField(max_length=50)
    data_emissao = models.DateField()
    natureza_operacao = models.CharField(max_length=50)
    regime_especial_tributacao = models.IntegerField()
    optante_simples_nacional = models.IntegerField()
    incetivador_cultural = models.IntegerField()
    competencia = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.OneToOneField(Servico, on_delete=models.CASCADE)

    def __str__(self):
        return  str(self.numero)
        # return str(self.numero) +'-'+str(self.tomador)

class DespesaComprovada(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=6,decimal_places=2)
    arquivo = models.FileField(upload_to=path_file_media)
    upload_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(os.path.basename(self.arquivo.name))