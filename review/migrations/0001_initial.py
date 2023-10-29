# Generated by Django 4.2.6 on 2023-10-28 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book_collection', '0009_remove_book_average_ratings_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book_collection.book')),
            ],
        ),
    ]
