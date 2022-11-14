# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    status = models.TextField()


class Friend(models.Model):
    primary = models.ForeignKey(User, on_delete=models.CASCADE, related_name="primary")
    secondary = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="secondary"
    )
    created_on = models.DateTimeField(auto_now_add=True)
