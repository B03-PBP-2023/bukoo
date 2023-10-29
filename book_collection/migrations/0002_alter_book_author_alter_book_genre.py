# Generated by Django 4.2.6 on 2023-10-23 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, to='book_collection.mockauthorprofile'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, to='book_collection.genre'),
        ),
    ]