# Generated by Django 4.2.1 on 2023-08-27 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_pagamento_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='valor_aluguel',
        ),
    ]
