# Generated by Django 4.2.6 on 2023-10-26 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_collection', '0007_alter_book_ratings_count_alter_book_reviews_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='num_pages',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
