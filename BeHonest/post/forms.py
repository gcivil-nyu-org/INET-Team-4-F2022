from .models import Comment, Post
from django import forms
from news.models import newsComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")


class NewsForm(forms.ModelForm):
    class Meta:
        model = newsComment
        fields = ("content",)
