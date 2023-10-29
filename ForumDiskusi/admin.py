from django.contrib import admin

# Register your models here.

from .models import BookDiscussion, DiscussionComment

admin.site.register(BookDiscussion)
admin.site.register(DiscussionComment)
