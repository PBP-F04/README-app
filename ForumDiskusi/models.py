from django.db import models

import uuid

app_name = 'ForumDiskusi'


class BookDiscussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey('KatalogBuku.Book', on_delete=models.CASCADE, related_name='current_book')
    user = models.ForeignKey('UserProfile.Profile', on_delete=models.CASCADE, related_name='user_discussions')
    title = models.TextField(default="")
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)



class DiscussionComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discussion = models.ForeignKey('BookDiscussion', on_delete=models.CASCADE, related_name='current_discussion')
    user = models.ForeignKey('UserProfile.Profile', on_delete=models.CASCADE, related_name='user_comments')
    title = models.TextField(default="")
    content = models.TextField()
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)