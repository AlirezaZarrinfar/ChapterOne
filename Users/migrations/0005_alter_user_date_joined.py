# Generated by Django 4.2.3 on 2023-07-05 17:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_remove_user_groups_remove_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 5, 20, 41, 27, 878288)),
        ),
    ]
