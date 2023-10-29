from django.forms import ModelForm
from .models import RequestedBook
from django import forms


class RequestedBookForm(ModelForm):
    class Meta:
        model = RequestedBook
        fields = ["title", "author", "book_url", "reason"]
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'text-[16px] rounded-[10px] px-2 py-1 border-[rgba(168, 168, 168, 0.5)] border-[1px] hover:border-[#727bfc] transition-all font-Inter'}),
            "author": forms.TextInput(attrs={
                'class': 'text-[16px] rounded-[10px] px-2 py-1 border-[rgba(168, 168, 168, 0.5)] border-[1px] hover:border-[#727bfc] transition-all font-Inter'}),
            "book_url": forms.TextInput(attrs={
                'class': 'text-[16px] rounded-[10px] px-2 py-1 border-[rgba(168, 168, 168, 0.5)] border-[1px] hover:border-[#727bfc] transition-all font-Inter'}),
            "reason": forms.Textarea(attrs={
                'class': 'text-[16px] rounded-[10px] px-2 py-1 border-[rgba(168, 168, 168, 0.5)] border-[1px] hover:border-[#727bfc] transition-all font-Inter'}),
            
        }
