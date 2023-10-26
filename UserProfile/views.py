from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def show_profile(request):
    profile = Profile.objects.filter(user=request.user)
    context = {
        'profile_img': request.user.profile_img,
        'username': request.user.username,
        'name': request.user.name,
        'description': request.user.description,
        'favorite_category': request.user.favorite_category
    }

    return render(request, "user_profile.html", context)

def create_profile(request):
    form = ProfileForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('KatalogBuku:#'))
    context = {'form': form}
    return render(request, "create_profile.html", context)

def edit_profile(request):
    form = ProfileForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('UserProfile:show_profile'))
    context = {'form': form}
    return render(request, "edit_profile.html", context)