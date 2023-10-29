from django.forms import ModelForm
from .models import BookDiscussion, DiscussionComment

class BookDiscussionForm(ModelForm):
    class Meta:
        model = BookDiscussion
        fields = ['title', 'content']