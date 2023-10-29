from django.urls import path
from .views import show_profile, create_profile, edit_profile, get_categories

app_name = 'UserProfile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
    path('create-profile/', create_profile, name='create_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('get-categories/', get_categories, name='get_categories'),
]
