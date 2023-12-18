from django.urls import path
from .views import (
    user_login,
    user_register,
    user_logout,
    cookie_logout,
    check_login,
    check_auth,
)

app_name = "authentication"

urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", user_register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("cookie-logout/", cookie_logout, name="cookie-logout"),
    path("login/check/", check_login, name="check-login"),
    path("protected/", check_auth, name="check-auth"),
]
