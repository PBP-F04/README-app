from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/login/')
def show_profile(request):
    context = {}

    try:
        profile = Profile.objects.get(user=request.user)
        context = {
            'profile_image': profile.profile_image,
            'username': profile.username,
            'name': profile.name,
            'description': profile.description,
            'favorite_category': profile.favorite_category
        }
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('profile:create_profile'))

    return render(request, "user_profile.html", context)

@login_required(login_url='/login/')
def create_profile(request):
    existing_profile = Profile.objects.filter(user=request.user).first()
    if existing_profile:
        return HttpResponseRedirect(reverse('profile:show_profile'))

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse('profile:show_profile'))
    else:
        form = ProfileForm()

    context = {'form': form}
    return render(request, "create_profile.html", context)

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return HttpResponseNotFound(b"Profile not found", status=404)

        profile_image = request.POST.get("profile_image")
        username = request.POST.get("username")
        name = request.POST.get("name")
        description = request.POST.get("description")
        favorite_category = request.POST.get("favorite_category")

        profile.profile_image = profile_image
        profile.username = username
        profile.name = name
        profile.description = description
        profile.favorite_category = favorite_category

        profile.save()

        return HttpResponse(b"OK", status=200)

    return HttpResponseNotFound(b"Invalid request method", status=400)