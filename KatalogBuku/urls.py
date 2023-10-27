from django.urls import path
from .views import index, get_books, get_categories, get_book_by_id, like_book, unlike_book

app_name = 'KatalogBuku'

urlpatterns = [
    path('', index, name='index'),
    path('books/', get_books, name='get_books'),
    path('books/category', get_categories, name='get_categories'),
    path('books/<str:book_id>', get_book_by_id, name='get_book'),
    path('books/<str:book_id>/like', like_book, name='like_book'),
    path('books/<str:book_id>/unlike', unlike_book, name='unlike_book')
]
