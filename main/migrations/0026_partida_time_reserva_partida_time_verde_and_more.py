# Generated by Django 4.2.1 on 2023-07-04 01:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_remove_partidajogadorreserva_jogador_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='time_reserva',
            field=models.ManyToManyField(blank=True, related_name='partidas_timeC', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partida',
            name='time_verde',
            field=models.ManyToManyField(blank=True, related_name='partidas_timeA', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='partida',
            name='time_vermelho',
            field=models.ManyToManyField(blank=True, related_name='partidas_timeB', to=settings.AUTH_USER_MODEL),
        ),
    ]
