# Generated by Django 4.2.1 on 2023-07-04 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_jogador_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogador',
            name='nome',
            field=models.CharField(default='Jorge', max_length=100, null=True),
        ),
    ]
