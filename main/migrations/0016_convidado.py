# Generated by Django 4.2.1 on 2023-07-04 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_delete_convidado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convidado',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('federado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convidados', to=settings.AUTH_USER_MODEL)),
                ('partida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convidados', to='main.partida')),
            ],
        ),
    ]
