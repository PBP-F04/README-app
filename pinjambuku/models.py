from django.db import models
from UserProfile.models import User  
from KatalogBuku.models import Book  

app_name = 'pinjambuku'

class BookLoan(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    finished_date = models.DateTimeField(blank=True, null=True)
