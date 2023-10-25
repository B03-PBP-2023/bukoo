# Generated by Django 4.2.6 on 2023-10-23 08:14

from django.db import migrations

from django.core.management import call_command


def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "genres")
    call_command("loaddata", "authors")
    call_command("loaddata", "books")


class Migration(migrations.Migration):

    dependencies = [
        ('book_collection', '0003_rename_genre_book_genres'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]
