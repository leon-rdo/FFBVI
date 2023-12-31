# Generated by Django 4.2.1 on 2023-07-04 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_convidado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='convidado',
            options={'verbose_name': 'Convidado', 'verbose_name_plural': 'Convidados'},
        ),
        migrations.AlterModelOptions(
            name='pagamento',
            options={'verbose_name': 'Pagamento', 'verbose_name_plural': 'Pagamentos'},
        ),
        migrations.RemoveField(
            model_name='convidado',
            name='partida',
        ),
        migrations.AddField(
            model_name='partida',
            name='convidados',
            field=models.ManyToManyField(blank=True, related_name='partidas', to='main.convidado'),
        ),
        migrations.AlterModelTable(
            name='pagamento',
            table=None,
        ),
    ]
