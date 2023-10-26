from django.urls import path
from .views import show_profile, create_profile, edit_profile

app_name = 'profile'

urlpatterns = [
    path('profile/', show_profile, name='show_profile'),
    path('create-profile/', create_profile, name='create_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]