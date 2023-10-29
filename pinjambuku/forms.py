from django.forms import ModelForm, ModelChoiceField
from .models import Profile
from KatalogBuku.models import Category, Books

class ProfileForm(ModelForm):
    favorite_category = ModelChoiceField(queryset=Books.objects.all(), to_field_name="title", required=False,
                                empty_label="Choose a book...")

    class Meta:
        model = Profile
        fields = ["profile_image", "username", "name", "description", "favorite_category"]