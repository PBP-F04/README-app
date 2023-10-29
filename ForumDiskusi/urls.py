from django.urls import path
from .views import show_book_discussion, show_discussion_comment, create_discussion, get_comment_json, add_comment_ajax


app_name = 'ForumDiskusi'

urlpatterns = [
    path('discussions/book=<str:book_id>', show_book_discussion, name='show_book_discussion'),
    path('discussions/topic=<str:discussion_id>', show_discussion_comment, name='show_discussion_comment'),
    path('discussions/create-discussion/<str:book_id>', create_discussion, name='create_discussion'),
    path('discussios/get-comment/<str:discussion_id>', get_comment_json, name='get_comment_json'),
    path('discussions/create-ajax/<str:discussion_id>', add_comment_ajax, name='add_comment_ajax'),
]