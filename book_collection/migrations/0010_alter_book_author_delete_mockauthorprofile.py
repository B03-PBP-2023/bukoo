# Generated by Django 4.2.6 on 2023-10-29 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '__first__'),
        ('book_collection', '0009_remove_book_average_ratings_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, to='user_profile.profile'),
        ),
        migrations.DeleteModel(
            name='MockAuthorProfile',
        ),
    ]
