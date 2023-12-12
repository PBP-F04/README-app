from django.urls import path
from .views import read_book

app_name = "pinjambuku"

urlpatterns = [
    path("", read_book, name="read_book"),
]
