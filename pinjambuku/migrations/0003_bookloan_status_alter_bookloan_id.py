# Generated by Django 4.1 on 2023-12-12 12:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pinjambuku', '0002_rename_finished_date_bookloan_done_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookloan',
            name='status',
            field=models.CharField(choices=[('BORROWED', 'Borrowed'), ('RETURNED', 'Returned')], default='BORROWED', max_length=100),
        ),
        migrations.AlterField(
            model_name='bookloan',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]