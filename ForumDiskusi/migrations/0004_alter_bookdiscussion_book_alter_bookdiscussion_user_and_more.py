# Generated by Django 4.2.4 on 2023-10-28 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KatalogBuku', '0003_requestedbook'),
        ('UserProfile', '0003_rename_profile_img_profile_profile_image'),
        ('ForumDiskusi', '0003_rename_comment_bookdiscussion_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdiscussion',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_book', to='KatalogBuku.book'),
        ),
        migrations.AlterField(
            model_name='bookdiscussion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_discussions', to='UserProfile.profile'),
        ),
        migrations.AlterField(
            model_name='discussioncomment',
            name='discussion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_discussion', to='ForumDiskusi.bookdiscussion'),
        ),
        migrations.AlterField(
            model_name='discussioncomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='UserProfile.profile'),
        ),
    ]