# Generated by Django 4.2.1 on 2023-07-04 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_partida_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogador',
            name='nome',
            field=models.CharField(max_length=100, null=True),
        ),
    ]