from django.db import models

from utils.models import UrlBaseModel
from utils.shortener import ShortCodeUtil


class ShortenedUrl(UrlBaseModel):

    original_url = models.URLField(max_length=2000, verbose_name="Original URL")
    shortened_url = models.CharField(max_length=200, unique=True, verbose_name="Shortened URL")
    click_count = models.PositiveIntegerField(default=0, verbose_name="Click Count")

    def __str__(self):
        return f"{self.original_url} -> {self.shortened_url}"

    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.shortened_url = ShortCodeUtil.generate_short_code()
        super().save(*args, **kwargs)