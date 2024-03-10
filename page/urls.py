# Django
from django.urls import path
# Page
from page.views import PageGenerator


urlpatterns = [
    path("<slug:slug>/", PageGenerator.as_view(), name="generate_page")
]