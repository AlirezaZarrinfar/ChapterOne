# Generated by Django 4.2.3 on 2023-07-21 19:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0041_alter_user_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 23, 6, 4, 114835)),
        ),
    ]
