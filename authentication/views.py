from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import User
from django.urls import reverse
import json


@login_required(login_url='/login/')
def show_test(request):
    return render(request, 'test.html')


def user_login(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        user = authenticate(request, username=email,
                            password=password)
        if user is not None:
            login(request, user)
            response = {
                'status': 200,
                'message': 'Login success'
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)
        else:
            return HttpResponse(json.dumps({'status': 400, 'message': 'Incorrect Email and Password'}),
                                content_type='application/json',
                                status=400)

    return render(request, 'index.html')


def user_register(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        confirm_password = body['confirmPassword']

        try:
            validate_email(email)
        except ValidationError as e:
            response = {
                'status': 400,
                'message': 'Email is not valid',
                'errorCode': 402
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        if len(email) == 0 or len(password) == 0 or len(confirm_password) == 0:
            response = {
                'status': 400,
                'message': 'Username, Password and Confirm Password cannot be empty',
                'errorCode': 400
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        if len(password) < 8:
            response = {
                'status': 400,
                'message': 'Password must be at least 8 characters',
                'errorCode': 400
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        if password != confirm_password:
            response = {
                'status': 400,
                'message': 'Password and Confirm Password not match',
                'errorCode': 400
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        if User.objects.filter(username=email).exists():
            response = {
                'status': 400,
                'message': 'Email already exists',
                'errorCode': 401
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        user = User.objects.create_user(username=email, password=password)
        user.save()
        response = {
            'status': 200,
            'message': 'Register success'
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))
