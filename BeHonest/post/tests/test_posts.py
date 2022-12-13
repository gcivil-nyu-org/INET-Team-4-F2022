from django.apps import apps
from django.test import TestCase, Client
from post.apps import BlogConfig
from post.models import Post, Comment
from news.models import News
from django.urls import reverse
from django.contrib.auth.models import User
from post.forms import PostForm, CommentForm, NewsForm
from post.badges import (
    get_posts,
    total_dislikes_received,
    total_likes_received,
    user_dislikes_badges_tier,
    user_friends_tier,
    user_likes_badges_tier,
    balance_badge,
    post_tier,
)


# Create user for testing purposes
def create_user(username_string):
    return User.objects.create(username=username_string)


# Create post for testing puproses
def create_post(authour_string):
    return Post.objects.create(author=authour_string)


# test that app config name matches and is found
class ReportsConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(BlogConfig.name, "post")
        self.assertEqual(apps.get_app_config("post").name, "post")


class BaseTest(TestCase):
    def setUp(self):
        self.post = Post(title="test")
        self.user = User.objects.create(username="test_user")
        self.user.set_password("newpassword")
        self.user.save()
        self.comment = Comment(content="testing", author=self.user)

        self.post_url = reverse("post:base")

        self.client = Client()
        self.search_url = reverse('post:search-results')
        self.prof_url = reverse('post:prof-results')
       # self.detail_url = reverse('post:post_detail', args=[22])
        # self.like_url = reverse('post:like_post',kwargs={'pk': 22})

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
    
    def test_search_GET(self):
        login = self.client.login(username="test_user", password="newpassword")
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "search_results.html")
    
    def test_search_results_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        response = self.client.post(self.search_url,data={"searched": 'd'} )
        self.assertEquals(response.status_code, 200)

    def test_prof_search_GET(self):
        login = self.client.login(username="test_user", password="newpassword")
        response = self.client.get(self.prof_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "prof_results.html")

    def test_prof_results_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        response = self.client.post(self.prof_url,data={"searched": 'd'} )
        self.assertEquals(response.status_code, 200)

    def test_post_list_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        response = self.client.post(self.post_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_post_detail_GET(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        response = self.client.post(reverse("post:post_detail", kwargs={'id': self.post.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')


class Like_Tests(BaseTest):
    def test_like_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        response = self.client.post(reverse("post:like_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)

    def test_liked_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        self.post.likes.add(self.user)
        response = self.client.post(reverse("post:like_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)

    def test_disliked_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        self.post.dislikes.add(self.user)
        response = self.client.post(reverse("post:like_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)
    

class Disike_Tests(BaseTest):
    def test_dislike_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        response = self.client.post(reverse("post:dislike_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)
    
    def test_liked_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        self.post.likes.add(self.user)
        response = self.client.post(reverse("post:dislike_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)
    
    def test_disliked_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        self.post.dislikes.add(self.user)
        response = self.client.post(reverse("post:dislike_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)


class Delete_Post_Test(BaseTest):
    def test_delete_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        response = self.client.post(reverse("post:delete_post", kwargs={'pk': self.post.pk}), data={"post_id":self.post.id})
        self.assertEquals(response.status_code, 302)


class Delete_User_Test(BaseTest):
    def test_user_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        self.post.likes.add(self.user)
        response = self.client.post(reverse("post:delete_user", kwargs={'pk': self.post.pk}), data={"username":self.user.username})
        self.assertEquals(response.status_code, 302)

class Profile_Test(BaseTest):
    def test_profile_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.post = Post.objects.create(
            title = "test",
            content = "",
            author = self.user
        )
        response = self.client.post(reverse("post:profile", kwargs={'pk': self.user.username}), data={"username":self.user.username})
        self.assertEquals(response.status_code, 200)


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

    def test_comment_form_invalid(self):
        form_data = self.invalid_comment
        form = NewsForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_news_detail_POST(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.news = News.objects.create(
            title = "test"
        )
        response = self.client.post(reverse("post:news_detail", kwargs={'id': self.news.id}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_detail.html')
    
    def test_news_detail_GET(self):
        login = self.client.login(username="test_user", password="newpassword")
        self.news = News.objects.create(
            title = "test"
        )
        response = self.client.get(reverse("post:news_detail", kwargs={'id': self.news.id}))
        self.assertEquals(response.status_code, 200)


# Test set for badge logic contained in badges.py
class Badges_Tests(BaseTest):

    # Test to see if a new user has no posts
    def test_user_with_no_posts_posts(self):
        test_user = create_user("test_user_1")
        self.assertFalse(get_posts(test_user))

    # Test to see if a new user has no likes
    def test_user_with_no_posts_likes(self):
        test_user = create_user("test_user_1")
        self.assertFalse(total_likes_received(test_user))

    # Test to see if a new user has no dislikes
    def test_user_with_no_posts_dislikes(self):
        test_user = create_user("test_user_1")
        self.assertFalse(total_dislikes_received(test_user))

    # Test to see if the dislikes tier function works
    def test_dislikes_badge(self):
        badges = []
        self.assertFalse(user_dislikes_badges_tier(badges, 100))

    # Test to see that the like tier function does not return a value
    def test_user_wth_no_posts_like_tier(self):
        badges = []
        self.assertFalse(user_likes_badges_tier(badges, 100))

    # Test to see that the balance badge works
    def test_user_wth_no_posts_dislike_tier(self):
        badges = []
        test_user = create_user("test_user_1")
        test_post1 = create_post(test_user)
        # Unknown how to test likes
        balance_badge(badges, test_user)
        self.assertTrue(test_post1)

    # Test friends tier
    def test_friends_tiers(self):
        badges = []
        friends = []
        for i in range(100):
            friends.append(i)

        user_friends_tier(badges, friends)

    # Test posts count tiers
    def test_posts_tier(self):
        badges = []
        test_user2 = create_user("test_user_2")

        for i in range(100):
            create_post(test_user2)

        post_tier(badges, test_user2)
