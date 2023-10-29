from django.urls import path
from .views import show_read_books, review_buku, show_read_books_ajax

app_name = 'ReviewBuku'

urlpatterns = [
    path('', show_read_books, name='show_read_books'),
    path('add-review/<str:book_id>', review_buku, name='review_buku'),
    path('show-read-books-ajax/', show_read_books_ajax, name='show_read_books_ajax'),
]