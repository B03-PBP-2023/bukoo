# Generated by Django 4.2.7 on 2023-12-15 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_book_by_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='prefered_genre',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
