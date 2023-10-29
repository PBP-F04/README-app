from django.urls import path
from .views import show_book_discussion, show_discussion_comment, create_discussion


app_name = 'ForumDiskusi'

urlpatterns = [
    path('discussions/book=<str:book_id>', show_book_discussion, name='show_book_discussion'),
    path('discussions/topic=<str:discussion_id>', show_discussion_comment, name='show_discussion_comment'),
    path('discussions/create', create_discussion, name='create_discussion'),
]