# Register your models here.
from django.contrib import admin
from .models import Friend, FriendRequest

admin.site.register(Friend)
admin.site.register(FriendRequest)
