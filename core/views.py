from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.db.models import F

from core.forms import ShortUrlForm
from core.models import ShortenedUrl


class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ShortUrlDetailView(View):
    template_name = 'core/short_url_detail.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', None)
        if not code:
            raise Http404("Shortened URL not found.")
        try:
            short_url = ShortenedUrl.objects.get(shortened_url=code)
        except ShortenedUrl.DoesNotExist:
            raise Http404("Shortened URL not found.")

        context = {
            'shortened_url': short_url,
            'object': short_url
        }
        return render(request, self.template_name, context)


class ShortUrlCreateView(CreateView):
    template_name = 'core/short_url_create.html'
    form_class = ShortUrlForm
    success_url = reverse_lazy('short_url_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = kwargs.get('initial', {})
        kwargs['initial']['request'] = self.request
        return kwargs

    def form_valid(self, form):
        original_url = form.cleaned_data['original_url']
        short_url = ShortenedUrl(original_url=original_url)
        user = self.request.user if self.request.user.is_authenticated else None
        short_url.save(user=user)
        return redirect(reverse('short_url_detail', kwargs={'code': short_url.shortened_url}))


class ShortUrlRedirectView(View):
    model = ShortenedUrl
    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', None)
        if not code:
            raise Http404("Shortened URL not found.")
        try:
            short_url = ShortenedUrl.objects.get(shortened_url=code)
        except ShortenedUrl.DoesNotExist:
            raise Http404("Shortened URL not found.")

        short_url.click_count = F('click_count') + 1
        short_url.save()
        return redirect(short_url.original_url)

