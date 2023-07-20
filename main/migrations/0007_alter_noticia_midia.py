# Generated by Django 4.2.1 on 2023-07-18 14:14

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_mídia_noticia_midia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='midia',
            field=models.FileField(upload_to=main.models.MediaTypeUploadTo(), validators=[main.models.validate_media_file], verbose_name='Imagem ou vídeo:'),
        ),
    ]