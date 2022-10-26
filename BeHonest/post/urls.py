from . import views
from django.urls import path

app_name = 'post'
urlpatterns = [
    path('', views.post_list, name='base'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
