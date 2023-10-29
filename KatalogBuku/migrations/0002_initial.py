# Generated by Django 4.2.6 on 2023-10-29 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserProfile', '0001_initial'),
        ('KatalogBuku', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestedbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_books', to='UserProfile.profile'),
        ),
        migrations.AddField(
            model_name='booklike',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_likes', to='KatalogBuku.book'),
        ),
        migrations.AddField(
            model_name='booklike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_likes', to='UserProfile.profile'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(related_name='books', to='KatalogBuku.category'),
        ),
    ]
