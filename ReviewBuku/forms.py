from django import forms
from .models import BookReview, UpvotedReview

class ReviewForm(forms.ModelForm):
    review_score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5}),  
    )

    class Meta:
        model = BookReview
        fields = ["review_score", "review_content"]
