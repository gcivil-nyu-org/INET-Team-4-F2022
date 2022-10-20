from . import views
from django.urls import path

app_name = 'post'
urlpatterns = [
    path('', views.PostList.as_view(), name='base'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
