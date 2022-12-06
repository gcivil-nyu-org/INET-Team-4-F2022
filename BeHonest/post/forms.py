from .models import Comment, Post
from django import forms
from news.models import newsComment
# from better_profanity import profanity


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    # def clean(self):

        # data from the form is fetched using super function
        super(CommentForm, self).clean()

        # extract the username and text field from the data
        content = self.cleaned_data.get("content")

        # conditions to be met for the username length
        # if profanity.contains_profanity(content):
           # self._errors["content"] = self.error_class(["please be polite"])

        # return any errors if found
       return self.cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")

    def clean(self):

        # data from the form is fetched using super function
        super(PostForm, self).clean()

        # extract the username and text field from the data
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")

        # conditions to be met for the username length
        # if profanity.contains_profanity(title):
            # self._errors["title"] = self.error_class(["please be polite"])
        # if profanity.contains_profanity(content):
           #  self._errors["content"] = self.error_class(["please be polite"])

        # return any errors if found
        return self.cleaned_data


class NewsForm(forms.ModelForm):
    class Meta:
        model = newsComment
        fields = ("content",)

    def clean(self):

        # data from the form is fetched using super function
        super(NewsForm, self).clean()

        # extract the username and text field from the data
        content = self.cleaned_data.get("content")

        # conditions to be met for the username length
        # if profanity.contains_profanity(content):
            # self._errors["content"] = self.error_class(["please be polite"])

        # return any errors if found
        return self.cleaned_data
