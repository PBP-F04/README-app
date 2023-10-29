import uuid
from django.db import models

from authentication.models import User

app_name = 'ReviewBuku'
# Create your models here.
class BookReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('UserProfile.Profile', on_delete=models.CASCADE, related_name='book_reviews')
    book = models.ForeignKey('KatalogBuku.Book', on_delete=models.CASCADE, related_name='book_reviews')
    review_score = models.FloatField()
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UpvotedReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('UserProfile.Profile', on_delete=models.CASCADE, related_name='upvoted_reviews')
    book = models.ForeignKey('KatalogBuku.Book', on_delete=models.CASCADE, related_name='upvoted_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    

