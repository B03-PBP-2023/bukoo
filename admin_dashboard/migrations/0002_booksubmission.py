# Generated by Django 4.2.7 on 2023-11-29 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_collection', '0003_auto_20231120_1439'),
        ('admin_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=255)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book_collection.book')),
            ],
        ),
    ]
