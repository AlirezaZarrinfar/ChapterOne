# Generated by Django 4.2.3 on 2023-07-21 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialMedia', '0021_alter_comment_created_at_favoritebook_and_more'),
        ('Users', '0037_alter_user_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_books',
            field=models.ManyToManyField(related_name='books_favorited_by', through='SocialMedia.FavoriteBook', to='SocialMedia.book'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 16, 30, 10, 574215)),
        ),
    ]