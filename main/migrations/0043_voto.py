# Generated by Django 4.0.6 on 2023-09-14 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_alter_pagamento_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jogador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votos_feitos', to=settings.AUTH_USER_MODEL)),
                ('partida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.partida')),
                ('votou_em', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votos_recebidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Voto',
                'verbose_name_plural': 'Votos',
            },
        ),
    ]