# Generated by Django 4.2.3 on 2023-07-21 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMedia', '0010_alter_comment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='full_name',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 3, 44, 25, 857868)),
        ),
    ]
