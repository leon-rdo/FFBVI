# Generated by Django 4.2.1 on 2023-08-11 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_configuracao_alerta_cor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='anulada',
            field=models.BooleanField(default=False, verbose_name='Foi anulada?'),
        ),
    ]
