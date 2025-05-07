from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

from core.models import ShortenedUrl


class ShortUrlForm(forms.ModelForm):
    original_url = forms.CharField(
        label="Orijinal URL",
        help_text="https://example.com, example.com veya /test/ olabilir.",
        error_messages={
            'required': 'Lütfen bir URL girin.',
        }
    )
    
    class Meta:
        model = ShortenedUrl
        fields = ['original_url']
    
    def clean_original_url(self):
        url = self.cleaned_data.get('original_url')
        if not url:
            return url
            
        if url.startswith('/'):
            request = self.initial.get('request', None)
            if request:
                url_for_db = f"{request.scheme}://{request.get_host()}{url}"
            else:
                url_for_db = url
            return url_for_db
        
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url_for_db = f"http://{url}"
        else:
            url_for_db = url
            
        validator = URLValidator()
        try:
            validator(url_for_db)
        except ValidationError:
            raise ValidationError('Url Formatı Hatalı /test/ formatında girin.')
            
        return url_for_db

