from django.urls import path
from .views import show_book_discussion, show_discussion_comment, create_discussion, get_comment_json, add_comment_ajax

from .views import create_discussion_flutter ,create_comment_flutter, show_json_discussions, show_json_comments


app_name = 'ForumDiskusi'

urlpatterns = [
    path('discussions/book=<str:book_id>', show_book_discussion, name='show_book_discussion'),
    path('discussions/topic=<str:discussion_id>', show_discussion_comment, name='show_discussion_comment'),
    path('discussions/create-discussion/<str:book_id>', create_discussion, name='create_discussion'),
    path('discussios/get-comment/<str:discussion_id>', get_comment_json, name='get_comment_json'),
    path('discussions/create-ajax/<str:discussion_id>', add_comment_ajax, name='add_comment_ajax'),

    path('discussions/json-discussions/<str:book_id>', show_json_discussions, name='show_json_discussions'),
    # path('discussions/json-discussions/', show_json_discussions, name='show_json_discussions'),

    path('discussions/json-comments/<str:discussion_id>', show_json_comments, name='show_json_comments'), #filter
    # path('discussions/json-comments/', show_json_comments, name='show_json_comments'),

    path('discussions/create-discussion-flutter/<str:book_id>', create_discussion_flutter, name='create_discussion_flutter'),
    # path('discussions/create-discussion-flutter/', create_discussion_flutter, name='create_discussion_flutter'),
    path('discussions/create-comment-flutter/<str:discussion_id>', create_comment_flutter, name='create_comment_flutter'),
]