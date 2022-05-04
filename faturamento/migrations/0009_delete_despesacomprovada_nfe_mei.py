# Generated by Django 4.0.4 on 2022-05-04 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mei', '0001_initial'),
        ('faturamento', '0008_despesacomprovada'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DespesaComprovada',
        ),
        migrations.AddField(
            model_name='nfe',
            name='mei',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='mei.mei'),
            preserve_default=False,
        ),
    ]