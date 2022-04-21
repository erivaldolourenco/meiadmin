# Generated by Django 4.0.4 on 2022-04-21 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
        ('faturamento', '0004_alter_endereco_bairro_alter_endereco_cep_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tomador',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='nfe',
            name='tomador',
        ),
        migrations.AddField(
            model_name='nfe',
            name='cliente',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Endereco',
        ),
        migrations.DeleteModel(
            name='Tomador',
        ),
    ]