from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_post")

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
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
