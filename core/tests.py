from django.http import Http404
from django.test import TestCase, Client
from django.urls import reverse
from core.models import ShortenedUrl


class RedirectUrlTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_url = "https://enes.com"
        self.shortened = ShortenedUrl.objects.create(original_url=self.test_url)

    def test_url_shortening(self):
        response = self.client.post(reverse('short_url_create'), {'original_url': 'https://enes.com'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ShortenedUrl.objects.filter(original_url='https://enes.com').exists())

    def test_redirect_works(self):
        response = self.client.get(reverse('redirect_short_url', kwargs={'code': self.shortened.shortened_url}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.test_url)

    def test_redirect_click_counter(self):
        initial_count = self.shortened.click_count
        self.client.get(reverse('redirect_short_url', kwargs={'code': self.shortened.shortened_url}))
        self.shortened.refresh_from_db()
        self.assertEqual(self.shortened.click_count, initial_count + 1)

    def test_invalid_short_url(self):
        response = self.client.get(reverse('redirect_short_url', kwargs={'code': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
