# Generated by Django 4.2.1 on 2023-05-17 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_song_audio_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='artist_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='genre',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
