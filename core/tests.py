from django.http import Http404
from django.test import TestCase, Client
from django.urls import reverse
from core.models import ShortenedUrl


class RedirectUrlTestCase(TestCase):
    pass
    # TODO: url shortening,
    # TODO: redirect works,
    # TODO: redirect click counter,
    # TODO: invalid short url
