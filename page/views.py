# Django
from django.shortcuts import render, redirect
from django.views import View
# Page
from page.models import page_caller

# Create your views here.
class PageGenerator(View):

    def get(self, request, slug):
        page = page_caller(slug)
        if page is None:
            return redirect('index')
        content = page.objects.last()
        return render(request, "page/content.html", {"content":content})