# Generated by Django 4.2.6 on 2023-10-28 06:46
from django.db import migrations
from django.core.management import call_command


def read_categories(apps, schema_editor):
    call_command('loaddata', 'categories.json')


def read_books(apps, schema_editor):
    call_command('loaddata', 'books.json')


class Migration(migrations.Migration):
    dependencies = [
        ('KatalogBuku', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(read_categories),
        migrations.RunPython(read_books),
    ]
