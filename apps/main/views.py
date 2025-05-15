from django.shortcuts import render
from django.views import View
from django.utils import timezone

# Create your views here.


class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "title": "Seyfer Studios Official Website",
            "now": timezone.now(),
        }
        return render(request, "main/index.html", context)


class AboutView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "title": "About Seyfer Studios",
            "now": timezone.now(),
        }
        return render(request, "main/about.html", context)
