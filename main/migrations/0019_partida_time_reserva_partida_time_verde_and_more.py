# Generated by Django 4.2.1 on 2023-07-04 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_jogador_remove_convidado_federado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='time_reserva',
            field=models.ManyToManyField(blank=True, related_name='partidas_time_reserva', through='main.PartidaJogadorReserva', to='main.jogador'),
        ),
        migrations.AddField(
            model_name='partida',
            name='time_verde',
            field=models.ManyToManyField(blank=True, related_name='partidas_time_verde', through='main.PartidaJogadorVerde', to='main.jogador'),
        ),
        migrations.AddField(
            model_name='partida',
            name='time_vermelho',
            field=models.ManyToManyField(blank=True, related_name='partidas_time_vermelho', through='main.PartidaJogadorVermelho', to='main.jogador'),
        ),
    ]