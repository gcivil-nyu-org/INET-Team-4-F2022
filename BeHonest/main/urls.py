from django.urls import path
from . import views
from post.views import post_list

app_name = "main"

# slashes after login and register are needed
urlpatterns = [
    path("home", post_list, name="base"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("", views.homepage, name="homepage"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    # Forget Password urls
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("reset/<uidb64>/<token>",views.passwordResetConfirm,name="password_reset_confirm",
    ),
]
