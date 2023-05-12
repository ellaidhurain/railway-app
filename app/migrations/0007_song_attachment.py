# Generated by Django 4.2 on 2023-05-12 06:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_song_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='attachment',
            field=models.FileField(null=True, upload_to='files', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg'])]),
        ),
    ]
