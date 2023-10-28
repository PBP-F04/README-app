# Generated by Django 4.2.6 on 2023-10-27 14:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0002_profile_favorite_category_alter_profile_id'),
        ('KatalogBuku', '0002_auto_20231027_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestedBook',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('book_url', models.URLField()),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_books', to='UserProfile.profile')),
            ],
        ),
    ]