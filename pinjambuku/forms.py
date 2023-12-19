from django.forms import ModelForm, ModelChoiceField
from .models import Profile
from KatalogBuku.models import Category, Book

class ProfileForm(ModelForm):
    book = ModelChoiceField(queryset=Book.objects.all(), to_field_name="title", required=False,
                                empty_label="Choose a book...")

    class Meta:
        model = Book
        fields = ["profile_image", "username", "name", "description", "book"]