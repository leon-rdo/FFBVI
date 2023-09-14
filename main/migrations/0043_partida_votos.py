# Generated by Django 4.2.1 on 2023-09-07 19:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_alter_pagamento_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='votos',
            field=models.ManyToManyField(blank=True, related_name='votos_partida', to=settings.AUTH_USER_MODEL),
        ),
    ]