from django.urls import path
from .views import show_profile

app_name = 'profile'

urlpatterns = [
    path('', show_profile, name='show_profile'),
    #path('', create_profile, name='create_profile'),
    #path('', edit_profile, name='edit_profile'),
]