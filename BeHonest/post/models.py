from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import pytz

utc = pytz.UTC


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_post")
    dislikes = models.ManyToManyField(User, related_name="blog_post")
    beginner_react = models.ManyToManyField(User, related_name="beg_post")
    medium_react = models.ManyToManyField(User, related_name="med_post")
    expert_react = models.ManyToManyField(User, related_name="exp_post")
    legend_react = models.ManyToManyField(User, related_name="leg_post")

    class Meta:
        ordering = ["-title"]

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def total_beginner_reacts(self):
        return self.beginner_react.count()

    def total_medium_reacts(self):
        return self.medium_react.count()

    def total_expert_reacts(self):
        return self.expert_react.count()

    def total_legend_reacts(self):
        return self.legend_react.count()

    def checknew(self):
        now = datetime.now()
        now = utc.localize(now)
        if now - timedelta(hours=24) <= self.created_on:
            return True
        else:
            return False


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
