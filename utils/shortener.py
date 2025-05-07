import random
import string


class ShortCodeUtil:
    @staticmethod
    def generate_short_code(length=6):
        from core.models import ShortenedUrl
        while True:
            characters = string.ascii_letters + string.digits
            short_code = ''.join(random.choice(characters) for _ in range(length))
            if not ShortenedUrl.objects.filter(shortened_url=short_code).exists():
                break
        return short_code
