
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from core.views import ShortUrlCreateView, ShortUrlDetailView, ShortUrlRedirectView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('test/', TemplateView.as_view(template_name='core/test.html'), name='test'),
    path('create/', ShortUrlCreateView.as_view(), name='short_url_create'),
    path('url/<str:code>/', ShortUrlDetailView.as_view(), name='short_url_detail'),
    path('<str:code>/', ShortUrlRedirectView.as_view(), name='redirect_short_url'),


]