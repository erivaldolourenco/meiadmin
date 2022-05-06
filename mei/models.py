from django.contrib.auth.models import User
from django.db import models
import datetime
import os

class Mei(models.Model):
   razao_social = models.CharField(max_length=100)
   cnpj = models.CharField(max_length=20)

   def __str__(self):
      return self.razao_social


class Responsavel(models.Model):
   usuario = models.OneToOneField(User, on_delete=models.CASCADE)
   mei = models.OneToOneField(Mei, on_delete=models.CASCADE)

   def __str__(self):
      return str(self.usuario)


def path_file_media(instance, filename):
   date = datetime.date.today()
   path = 'upload/' + str(date.year) + '/' + str(date.month)
   file_name = '{0}'.format(filename.lower().replace(' ', '-'))
   return os.path.join(path, file_name)


class DespesaComprovada(models.Model):
   nome = models.CharField(max_length=200, blank=True, null=True)
   descricao = models.TextField()
   valor = models.DecimalField(max_digits=6, decimal_places=2)
   arquivo = models.FileField(upload_to=path_file_media)
   upload_date = models.DateField(auto_now=True)
   data_pagamento = models.DateField()
   mei = models.ForeignKey(Mei, on_delete=models.CASCADE)

   def __str__(self):
      return str(os.path.basename(self.arquivo.name))