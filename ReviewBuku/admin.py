from django.contrib import admin
from .models import BookReview, UpvotedReview

# Register your models here.
admin.site.register(BookReview)
admin.site.register(UpvotedReview)
