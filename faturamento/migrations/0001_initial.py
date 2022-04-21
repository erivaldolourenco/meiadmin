# Generated by Django 4.0.4 on 2022-04-21 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(max_length=100)),
                ('numero', models.CharField(max_length=50)),
                ('complemento', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_servicos', models.DecimalField(decimal_places=2, max_digits=6)),
                ('iss_retido', models.DecimalField(decimal_places=2, max_digits=6)),
                ('valor_iss', models.DecimalField(decimal_places=2, max_digits=6)),
                ('base_calculo', models.DecimalField(decimal_places=2, max_digits=6)),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=6)),
                ('valor_liquido_nfse', models.DecimalField(decimal_places=2, max_digits=6)),
                ('valor_iss_retido', models.DecimalField(decimal_places=2, max_digits=6)),
                ('item_lista_servico', models.IntegerField()),
                ('codigo_tributacao_municipio', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, max_length=500)),
                ('municipio_prestacao_servico', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tomador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CNPJ', models.CharField(max_length=50)),
                ('razao_social', models.CharField(max_length=200)),
                ('endereco', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='faturamento.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='NFE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('codigo_verificacao', models.CharField(max_length=50)),
                ('data_emissao', models.DateField()),
                ('natureza_operacao', models.IntegerField()),
                ('regime_especial_tributacao', models.IntegerField()),
                ('optante_simples_nacional', models.IntegerField()),
                ('incetivador_cultural', models.IntegerField()),
                ('competencia', models.CharField(max_length=50)),
                ('servico', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='faturamento.servico')),
                ('tomador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='faturamento.tomador')),
            ],
        ),
    ]