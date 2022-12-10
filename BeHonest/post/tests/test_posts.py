from django.apps import apps
from django.test import TestCase
from post.apps import BlogConfig
from post.models import Post, Comment
from django.urls import reverse
from django.contrib.auth.models import User
from post.forms import PostForm, CommentForm, NewsForm
from post.badges import *
from django.contrib.auth.models import User

# Create user for testing purposes
def create_user(username_string):
    return User.objects.create(username=username_string)


# test that app config name matches and is found
class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(BlogConfig.name, "post")
        self.assertEqual(apps.get_app_config("post").name, "post")


class BaseTest(TestCase):
    def setUp(self):
        self.post = Post(title="test")
        self.user = User.objects.create(username="test_user")
        self.comment = Comment(content="testing", author=self.user)

        self.post_url = reverse("post:base")

        self.valid_post = {
            "title": "Testing",
            "content": "Test content",
        }
        self.invalid_post = {
            "title": "",
            "content": "",
        }

        self.valid_comment = {
            "content": "valid content",
        }
        self.invalid_comment = {
            "content": "",
        }

        return super().setUp()


class Post_Tests(BaseTest):
    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_url(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 302)

    def test_post_form_valid(self):
        form_data = self.valid_post
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

#     def test_post_form_invalid(self):
#         form_data = self.invalid_post
#         form = PostForm(data=form_data)
#         self.assertFalse(form.is_valid())


class Comment_Tests(BaseTest):
    def test_string_representation(self):
        self.assertEqual(
            str(self.comment),
            "Comment {} by {}".format(self.comment.content, self.comment.author),
        )

    def test_comment_form_valid(self):
        form_data = self.valid_comment
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

#     def test_comment_form_invalid(self):
#         form_data = self.invalid_comment
#         form = CommentForm(data=form_data)
#         self.assertFalse(form.is_valid())

class News_Tests(BaseTest):
    def test_string_representation(self):
        self.assertEqual(
            str(self.comment),
            "Comment {} by {}".format(self.comment.content, self.comment.author),
        )

    def test_comment_form_valid(self):
        form_data = self.valid_comment
        form = NewsForm(data=form_data)
        self.assertTrue(form.is_valid())

#     def test_comment_form_invalid(self):
#         form_data = self.invalid_comment
#         form = NewsForm(data=form_data)
#         self.assertFalse(form.is_valid())

# Test set for badge logic contained in badges.py
class Badges_Tests(BaseTest):

    # Test to see if the first user 
    def test_user_with_no_posts(self):
        test_user = create_user("test_user_1")
        # user = User.objects.get(username="test_user_1")
        self.assertFalse(get_posts(test_user))