# Generated by Django 4.2.3 on 2023-07-21 01:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMedia', '0013_alter_comment_created_at_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 4, 32, 7, 372733)),
        ),
    ]
