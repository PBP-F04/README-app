from django.forms import ModelForm
from .models import BookReview, UpvotedReview

class ReviewForm(ModelForm):
    class Meta:
        model = BookReview
        fields = ["review_score", "review_content"]