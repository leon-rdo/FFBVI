# Generated by Django 4.2.1 on 2023-07-04 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_jogador_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partidajogadorreserva',
            name='jogador',
        ),
        migrations.RemoveField(
            model_name='partidajogadorreserva',
            name='partida',
        ),
        migrations.RemoveField(
            model_name='partidajogadorverde',
            name='jogador',
        ),
        migrations.RemoveField(
            model_name='partidajogadorverde',
            name='partida',
        ),
        migrations.RemoveField(
            model_name='partidajogadorvermelho',
            name='jogador',
        ),
        migrations.RemoveField(
            model_name='partidajogadorvermelho',
            name='partida',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='time_reserva',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='time_verde',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='time_vermelho',
        ),
        migrations.RemoveField(
            model_name='user',
            name='jogador',
        ),
        migrations.AlterField(
            model_name='partida',
            name='slug',
            field=models.SlugField(default='', editable=False, unique=True),
        ),
        migrations.DeleteModel(
            name='Convidado',
        ),
        migrations.DeleteModel(
            name='Jogador',
        ),
        migrations.DeleteModel(
            name='PartidaJogadorReserva',
        ),
        migrations.DeleteModel(
            name='PartidaJogadorVerde',
        ),
        migrations.DeleteModel(
            name='PartidaJogadorVermelho',
        ),
    ]
