from django.db import models
import uuid

app_name = 'KatalogBuku'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issued = models.CharField(max_length=100)
    book_code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    book_read_url = models.URLField()
    subject = models.CharField(max_length=100)
    synopsis = models.TextField()
    category = models.ManyToManyField('Category', related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category_name}'


class BookLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_likes')
    user = models.ForeignKey('UserProfile.Profile', on_delete=models.CASCADE, related_name='book_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RequestedBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    book_url = models.URLField()
    reason = models.TextField()
    user = models.ForeignKey('UserProfile.Profile', on_delete=models.CASCADE, related_name='requested_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
