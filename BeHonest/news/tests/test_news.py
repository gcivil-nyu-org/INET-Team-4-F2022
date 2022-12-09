from django.test import TestCase
from django.apps import apps
from news.views import index
from newsapi import NewsApiClient
from django.urls import reverse

class TestPage(TestCase):

    def setUp(self):
        self.client = NewsApiClient(api_key="084b04d11f594e6a90cb0e4f8b0fab81")

    def test_index_page(self):
        url = reverse('news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
