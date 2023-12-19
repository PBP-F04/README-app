from django.shortcuts import render
from KatalogBuku.models import Category
from authentication.models import User
from .models import Profile
from .forms import ProfileForm
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

# Create your views here.
@login_required(login_url='authentication:login')
def show_profile(request):
    context = {}

    try:
        profile = Profile.objects.get(user=request.user)
        context = {
            'profile_image': profile.profile_image,
            'username': profile.username,
            'name': profile.name,
            'description': profile.description,
            'favorite_category': profile.favorite_category,
        }
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('UserProfile:create_profile'))

    return render(request, "user_profile.html", context)


@login_required(login_url='authentication:login')
def create_profile(request):
    existing_profile = Profile.objects.filter(user=request.user).first()
    if existing_profile:
        return HttpResponseRedirect(reverse('KatalogBuku:index'))

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse('KatalogBuku:index'))
    else:
        form = ProfileForm()

    context = {'form': form}
    return render(request, "create_profile.html", context)


@csrf_exempt
@login_required(login_url='authentication:login')
def edit_profile(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
        favorite_category = Category.objects.get(id=request.POST.get('favorite_category'))
        profile_image = request.POST.get("profile_image")
        username = request.POST.get("username")
        name = request.POST.get("name")
        description = request.POST.get("description")
        profile.profile_image = profile_image
        profile.username = username
        profile.name = name
        profile.description = description
        profile.favorite_category = favorite_category

        profile.save()

        return HttpResponse(b"OK", status=200)

    return HttpResponseNotFound(b"Invalid request method", status=400)


def get_categories(request):
    categories = Category.objects.all().values('id', 'category_name')
    return JsonResponse(list(categories), safe=False)

def show_profile_flutter(request, email):
    profile = Profile.objects.filter(user_id=User.objects.get(username=email).id)

    return HttpResponse(serializers.serialize("json", profile), content_type="application/json")

@csrf_exempt
def create_profile_flutter(request):
    
    if request.method == 'POST':
        email = request.headers.get('X-Custom-Email')
        form = ProfileForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("a")
            profile = form.save(commit=False)
            profile.user = User.objects.get(username=email)
            profile.save()
        else:
            print('b')

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=400)
    

@csrf_exempt
def edit_profile_flutter(request):
    if request.method == 'POST':
        email = request.headers.get('X-Custom-Email')
        profile_image = request.POST.get('profile_image')
        username = request.POST.get('username')
        name = request.POST.get('name')
        description = request.POST.get('description')
        favorite_category_name = request.POST.get('favorite_category')

        try:
            profile = Profile.objects.get(user__username=email)
            category = Category.objects.get(category_name=favorite_category_name)
            
            profile.profile_image = profile_image
            profile.username = username
            profile.name = name
            profile.description = description
            profile.favorite_category = category
            profile.save()

            return JsonResponse({"status": "success"}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Category does not exist"}, status=400)
        except Profile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Profile does not exist"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)