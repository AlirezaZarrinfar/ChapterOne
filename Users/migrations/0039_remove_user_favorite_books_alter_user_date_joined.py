# Generated by Django 4.2.3 on 2023-07-21 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0038_user_favorite_books_alter_user_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='favorite_books',
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 16, 31, 53, 352963)),
        ),
    ]
