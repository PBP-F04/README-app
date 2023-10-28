import uuid
from django.db import models

from authentication.models import User

app_name = 'review'
# Create your models here.
class BookReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    book = models.ForeignKey() #sama
    review_score = models.TextField()
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UpvotedReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey() #sama
    created_at = models.DateTimeField(auto_now_add=True)
    

