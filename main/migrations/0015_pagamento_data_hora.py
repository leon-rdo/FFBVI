# Generated by Django 4.2.1 on 2023-08-26 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_pagamento_confirmado_pagamento_valor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='data_hora',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data e hora do pagamento'),
        ),
    ]