from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

#class for base tests to generate users, etc. for tests below
#called once before each case is run good place to store testing data
class BaseTest(TestCase):
    def setUp(self):
        #url used to produce response for register
        self.register_url = reverse('main:register')
        #url used to produce response for login
        self.login_url=reverse('main:login')

        #some test users
        self.user={
            'email':'testemail@gmail.com',
            'username':'testuser3',
            'password':'somethinglong',
            'password2':'somethinglong',
        }
        return super().setUp()

#first unit-test on registration
class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/register.html')

    #thought this was re-direct
    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code, 200)

#tests for login
class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/login.html')

    # #should be re-direct
    # def test_login_success(self):
    #     self.client.post(self.register_url,self.user,format='text/html')
    #     user=User.objects.filter(email=self.user['email']).first()
    #     user.save()
    #     response= self.client.post(self.login_url,self.user,format='text/html')
    #     self.assertEqual(response.status_code,302)
