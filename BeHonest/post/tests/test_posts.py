from django.apps import apps
from django.test import TestCase
from post.apps import BlogConfig
from post.models import Post, Comment
from django.urls import reverse
from django.contrib.auth.models import User
from post.forms import PostForm, CommentForm


# bandaid fix to re-use don't need anymore
# class LogoutTest(TestCase):
#     def test_logout_url(self):
#         self.logout_url = reverse("post:logout")
#         response = self.client.get(self.logout_url)
#         self.assertEqual(response.status_code, 302)


# test that app config name matches and is found
class ReportsConfigTest(TestCase):
    def test_apps(self):
        print(BlogConfig.name)
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

    def test_post_form_invalid(self):
        form_data = self.invalid_post
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


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

    def test_comment_form_invalid(self):
        form_data = self.invalid_comment
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
