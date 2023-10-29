from django.contrib import admin
from .models import Book, Category, BookLike, RequestedBook

# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookLike)
admin.site.register(RequestedBook)
