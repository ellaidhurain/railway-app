# Generated by Django 4.2 on 2023-05-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_chatroom_user2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
