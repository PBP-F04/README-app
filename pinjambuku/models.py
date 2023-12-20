import uuid
from django.db import models

app_name = "pinjambuku"


class BookLoan(models.Model):
    class status(models.TextChoices):
        BORROWED = "BORROWED"
        RETURNED = "RETURNED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "UserProfile.Profile", on_delete=models.CASCADE, related_name="book_loans"
    )
    book = models.ForeignKey(
        "KatalogBuku.Book", on_delete=models.CASCADE, related_name="book_loands"
    )
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    finished_date = models.DateTimeField(blank=True, null=True)
