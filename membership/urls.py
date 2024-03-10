# Django
from django.urls import path
# Membership
from membership.views.account import Account

urlpatterns = [
    path('me/', Account.as_view(), name="account_display"),
]