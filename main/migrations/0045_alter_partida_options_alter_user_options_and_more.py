# Generated by Django 5.0.1 on 2024-02-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_alter_voto_jogador_alter_voto_partida_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partida',
            options={'ordering': ['-data'], 'verbose_name': 'Partida', 'verbose_name_plural': 'Partidas'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['nome_jogador'], 'verbose_name': 'Usuário', 'verbose_name_plural': 'Usuários'},
        ),
        migrations.RemoveField(
            model_name='noticia',
            name='duracao_video',
        ),
        migrations.AlterField(
            model_name='partida',
            name='slug',
            field=models.SlugField(editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='patrocinador',
            name='link',
            field=models.URLField(verbose_name='Link:'),
        ),
        migrations.AlterField(
            model_name='patrocinador',
            name='nome',
            field=models.CharField(max_length=18, verbose_name='Nome:'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nome_jogador',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nome de Jogador:'),
        ),
    ]
