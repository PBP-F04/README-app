from django.urls import path
from .views import show_read_books, review_buku

app_name = 'review'

urlpatterns = [
    path('', show_read_books, name='show_read_books'),
    path('add-review/', review_buku, name='review_buku'),
]