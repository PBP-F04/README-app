from django.forms import ModelForm, ModelChoiceField
from .models import Profile
from KatalogBuku.models import Category


class ProfileForm(ModelForm):
    favorite_category = ModelChoiceField(queryset=Category.objects.all(), to_field_name="category_name", required=False,
                                empty_label="null")

    class Meta:
        model = Profile
        fields = ["profile_image", "username", "name", "description", "favorite_category"]
