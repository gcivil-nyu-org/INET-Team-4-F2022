from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=10, blank=True, null=True)
    img = models.CharField(max_length=4000, blank=True, null=True)
    url = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title


class newsComment(models.Model):
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name="newscomment")
    author = models.ForeignKey(
        User, default=User.objects.first().id, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.content, self.author)
