# Generated by Django 4.2.6 on 2023-10-23 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_collection', '0002_alter_book_author_alter_book_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='genre',
            new_name='genres',
        ),
    ]