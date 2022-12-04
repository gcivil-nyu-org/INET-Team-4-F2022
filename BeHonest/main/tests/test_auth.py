from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from main.forms import NewUserForm, PasswordResetForm

# class for base tests to generate users, etc. for tests below
# called once before each case is run good place to store testing data


class BaseTest(TestCase):
    def setUp(self):
        # url used for homepage
        self.homepage_url = reverse("main:homepage")
        # url used to produce response for register
        self.register_url = reverse("main:register")
        # url used to produce response for login
        self.login_url = reverse("main:login")
        # url used to logout
        self.logout_url = reverse("main:logout")

        # some test users
        self.user = {
            "username": "Testuser_3",
            "email": "testemail@gmail.com",
            "password1": "UncxYv234zzy",
            "password2": "UncxYv234zzy",
        }
        self.invalid_user = {
            "username": "",
            "email": "testemail@gmail.com",
            "password1": "pwd",
            "password2": "pwd",
        }
        
        return super().setUp()


class HomePageTest(BaseTest):
    def test_homepage_access(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

    def test_homepage_login_fail(self):
        self.client.post(self.homepage_url, self.invalid_user, format="text/html")
        user = User.objects.filter(username=self.invalid_user["username"]).first()
        self.assertEqual(user, None)
        response = self.client.post(
            self.homepage_url, self.invalid_user, format="text/html"
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Invalid username or password.")

    def test_client_login(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        self.assertTrue(logged_in)

    #testing for re-direct
    def test_redirect_unauthenticated(self):
        self.username = 'test1'
        self.password = '12345qwe'
        user = User.objects.create_user(username=self.username)
        user.set_password(self.password)
        user.save()
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.get(self.homepage_url)
        self.assertEqual(response.status_code, 302)
    
    def test_login_redirect(self):
        self.username = 'test2'
        self.password = 'somethin1234Long@'
        user = User.objects.create_user(username=self.username)
        user.set_password(self.password)
        user.save()
        client = Client()
        client.login(username=self.username, password=self.password)
        response = client.get(self.homepage_url)
        self.assertEqual(response.status_code, 302)

class RegisterTest(BaseTest):
    def test_register_url(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/register.html")

    def test_register_success_url(self):
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 302)

    def test_register_form_valid(self):
        form_data = self.user
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.client.post(self.register_url, self.user, format="text/html")
        user = User.objects.filter(username=self.user["username"]).first()
        user.save()

    def test_register_form_invalid(self):
        form_data = self.invalid_user
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_registration(self):
        self.client.post(self.register_url, self.invalid_user, format="text/html")
        user = User.objects.filter(username=self.user["username"]).first()
        self.assertEqual(user, None)

    def test_invalid(self):
        form = NewUserForm(
            {
                "username": "TestUser",
                "email": "testemail@gmailcom",
                "password1": "pwd",
                "password2": "pwd",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors["email"], ["Enter a valid email address."])


# tests for login
class LoginTest(BaseTest):
    def test_login_url(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/login.html")

    # tested registration message as well here also needed response 2 for homepage
    # Temporarily removed as the login process has changed to accomadate email verification
    # def test_login_success(self):
    #     self.client.post(self.register_url, self.user, format="text/html")
    #     user = User.objects.filter(username=self.user["username"]).first()
    #     user.save()
    #     response = self.client.post(self.login_url, self.user, format="text/html")
    #     self.assertEqual(response.status_code, 200)
    #     messages = list(response.context["messages"])
    #     self.assertEqual(str(messages[0:4]), "Dear ")

    def test_login_fail(self):
        self.client.post(self.register_url, self.invalid_user, format="text/html")
        user = User.objects.filter(username=self.invalid_user["username"]).first()
        self.assertEqual(user, None)
        response = self.client.post(
            self.login_url, self.invalid_user, format="text/html"
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "Invalid username or password.")

    def test_client_login(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        c = Client()
        logged_in = c.login(username="testuser", password="12345")
        self.assertTrue(logged_in)


class LogoutTest(BaseTest):
    # test for redirect to homepage
    def test_logout_url(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)


class PasswordResetRequestTest(BaseTest):
    def test_password2(self):
        # form_data = self.user
        # form = PasswordResetForm(data=form_data)
        # print(form)
        # user = self.user
        # old_sha = self.user["password1"]

        form = PasswordResetForm(data=self.user)
        self.assertTrue(form.is_valid())

        form = PasswordResetForm(data={"password1": "foo"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required."])

    # def test_password_reset_match(self):
    #     user = self.user
    #     old_sha = self.user["password1"]

    #     form = PasswordResetForm(data=self.user)
    #     self.assertTrue(form.is_valid())

    #     form = PasswordResetForm(data={'password1': 'foo',
    #                                               'password2': 'bar'})
    #     self.assertFalse(form.is_valid())
    #     print(form.errors)
    #     self.assertEqual(form.errors,
    #                      ['This field is required.'])
    # form = PasswordResetForm(data={'password1': 'foo',
    #                                           'password2': 'bar'})
    # self.assertFalse(form.is_valid())
    # # print(form.errors)
    # self.assertEqual(form.errors['email'],
    #                  ['This field is required.'])

    # form = PasswordResetForm(data={'password1': 'foo',
    #                                           'password2': 'foo'})
    # self.assertTrue(form.is_valid())
    # self.assertEqual(user.password, old_sha)
    # form.save()
    # self.assertNotEqual(user.password, old_sha)
