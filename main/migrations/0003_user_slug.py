# Generated by Django 4.2.1 on 2023-06-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_tipo_alter_user_gols_marcados_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
