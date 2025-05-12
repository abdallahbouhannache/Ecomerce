# Django
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Django REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Home
from home.utils import shipping_initial_price, shipping_extra_fees
from home.models import Product

class PaidShippingAPI(APIView):

    def get(self, request, product_slug, mode):
        # Query
        query = Product.objects.exclude(Q(stock=0)|Q(show=False)|Q(deleted=True))
        product = get_object_or_404(query, slug=product_slug)
        # Shipping Calculation
        initial_price = shipping_initial_price(mode, product.warehouse, request.user.member.wilaya, request.user.member.commune)
        extra_fees    = shipping_extra_fees(mode, product)
        # Paid Shipping Price
        shipping_price = initial_price + extra_fees
        resp = {
            "status_code":"200",
            "message":shipping_price,
        }
        return Response(resp, status=status.HTTP_200_OK)