from django.urls import path
from .views import *

app_name = "ReviewBuku"

urlpatterns = [
    path("", show_page_review, name="show_read_books"),
    path("add-review/<str:book_id>/", review_buku, name="review_buku"),
    path(
        "show-page-review-ajax/<str:book_id>/",
        show_page_review_ajax,
        name="show_page_review_ajax",
    ),
    path(
        "show_page_review_userajax/",
        show_page_review_user_ajax,
        name="show_page_review_user_ajax",
    ),
    path("get-reviews-json/", get_reviews_json, name="get_reviews_json"),
    path(
        "review-buku-flutter/",
        review_buku_flutter,
        name="review_buku_flutter",
    ),
]
