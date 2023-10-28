from django.db import models
from django.contrib.auth.models import User  # Import the User model, or your custom UserProfile model if you have one.
# from your_app.models import Book  # Import the Book model from your app, adjust the import as needed.

class BookLoan(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    finished_date = models.DateTimeField(blank=True, null=True)
