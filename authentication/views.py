from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import User
from django.urls import reverse
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.csrf import csrf_exempt
from UserProfile.models import Profile


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body["email"]
        password = body["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            existing_profile = Profile.objects.filter(
                user=User.objects.get(username=email)
            ).first()
            if existing_profile:
                return JsonResponse(
                    {
                        "status": 200,
                        "exist": True,
                        "message": "Login success",
                        "userame": request.user.username,
                    },
                    status=200,
                )

            return JsonResponse(
                {
                    "status": 200,
                    "exist": False,
                    "message": "Login success",
                    "userame": request.user.username,
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"status": 400, "message": "Incorrect Email and Password"}, status=400
            )
    return render(request, "index.html")


@csrf_exempt
def user_register(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body["email"]
        password = body["password"]
        confirm_password = body["confirmPassword"]

        try:
            validate_email(email)
        except ValidationError as e:
            response = {
                "status": 400,
                "message": "Email is not valid",
                "errorCode": 402,
            }
            return JsonResponse(response, status=400)

        if len(email) == 0 or len(password) == 0 or len(confirm_password) == 0:
            response = {
                "status": 400,
                "message": "Username, Password and Confirm Password cannot be empty",
                "errorCode": 400,
            }
            return JsonResponse(response, status=400)

        if len(password) < 8:
            response = {
                "status": 400,
                "message": "Password must be at least 8 characters",
                "errorCode": 400,
            }
            return JsonResponse(response, status=400)

        if password != confirm_password:
            response = {
                "status": 400,
                "message": "Password and Confirm Password not match",
                "errorCode": 400,
            }
            return JsonResponse(response, status=400)

        if User.objects.filter(username=email).exists():
            response = {
                "status": 400,
                "message": "Email already exists",
                "errorCode": 401,
            }
            return JsonResponse(response, status=400)

        user = User.objects.create_user(username=email, password=password)
        user.save()
        response = {"status": 200, "message": "Register success"}
        return JsonResponse(response, status=200)

    return render(request, "register.html")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("authentication:login"))


@csrf_exempt
def cookie_logout(request):
    logout(request)
    return JsonResponse({"status": 200, "message": "Logout success"}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def check_login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            response = {
                "status": 200,
                "message": "User is logged in",
                "user": user.username,
            }

            return JsonResponse(response)
        else:
            return JsonResponse(
                {"status": 400, "message": "User is not logged in"}, status=400
            )


def login_required_json(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"status": 401, "message": "Unauthorized"}, status=401)

    return _wrapped_view


@login_required_json
@csrf_exempt
@require_http_methods(["GET"])
def check_auth(request):
    if request.method == "GET":
        response = {"status": 200, "message": "User is logged in"}
        return JsonResponse(response)
