# Generated by Django 4.0.4 on 2022-04-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0005_remove_tomador_endereco_remove_nfe_tomador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='item_lista_servico',
            field=models.CharField(max_length=50),
        ),
    ]