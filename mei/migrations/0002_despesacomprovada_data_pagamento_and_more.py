# Generated by Django 4.0.4 on 2022-05-08 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mei', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesacomprovada',
            name='data_pagamento',
            field=models.DateField(default='2022-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='despesacomprovada',
            name='mei',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mei.mei'),
        ),
    ]
