from django.db import models

# Create your models here.
from mei.models import Mei


class Endereco(models.Model):
    endereco  = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    complemento = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cep = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.cep

class Cliente(models.Model):
    cnpj  = models.CharField(max_length=50)
    razao_social  = models.CharField(max_length=200, null=True, blank=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True)
    mei = models.OneToOneField(Mei, on_delete=models.CASCADE)

    def __str__(self):
        if self.razao_social is not None:
            return self.razao_social
        else:
            return ""
