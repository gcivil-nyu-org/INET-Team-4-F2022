from django.urls import path
from . import views
from news.views import index
from post.views import post_list

app_name = "main"


urlpatterns = [
    path("home", post_list, name="base"),
    path("register", views.register_request, name="register"),
    path('news', index, name="news"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("", views.homepage, name="homepage"),
]
