from django.urls import path
from .views import create_profile_flutter, edit_profile_flutter, show_profile, create_profile, edit_profile, get_categories, show_profile_flutter

app_name = 'UserProfile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
    path('create-profile/', create_profile, name='create_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('get-categories/', get_categories, name='get_categories'),
    path('show-profile/<str:email>/', show_profile_flutter, name='show_profile_flutter'),
    path('create-profile-flutter/', create_profile_flutter, name='create_profile_flutter'),
    path('edit-profile-flutter/', edit_profile_flutter, name='edit_profile_flutter'),
]
