# Generated by Django 4.2.1 on 2023-07-04 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_partida_time_reserva_partida_time_verde_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]