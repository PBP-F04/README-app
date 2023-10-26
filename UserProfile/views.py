from django.shortcuts import render
from .models import Profile
from UserProfile.forms import ProfileForm, Profile

# Create your views here.
def show_profile(request):

    context = {
        'profile_img': request.user.profile_img,
        'username': request.user.username,
        'name': request.user.name,
        'description': request.user.description,
        'fav_category': request.user.fav_category
    }

    return render(request, "user_profile.html", context)

def create_profile(request):
    form = ProfileForm(request.POST or None)

    context = {'form': form}
    return render(request, "create_profile.html", context)

