# Generated by Django 4.2.1 on 2023-05-17 08:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_song_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='attachment',
            field=models.FileField(default=None, upload_to='files', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
    ]
