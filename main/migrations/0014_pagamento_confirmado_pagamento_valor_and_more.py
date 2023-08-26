# Generated by Django 4.2.1 on 2023-08-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_partida_razao_anulacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='confirmado',
            field=models.BooleanField(default=False, verbose_name='Pagamento confirmado?'),
        ),
        migrations.AddField(
            model_name='pagamento',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='partida',
            name='valor_aluguel',
            field=models.DecimalField(decimal_places=2, default=140.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='em_dinheiro',
            field=models.BooleanField(default=False, verbose_name='Pagamento em dinheiro?'),
        ),
    ]