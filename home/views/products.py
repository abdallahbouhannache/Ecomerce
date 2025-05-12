# Python
from random import shuffle
# Django
from django.views import View
from django.urls import reverse
from django.utils.translation import get_language
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
# Home
from home.models import Category, Product
from home.utils import shipping_initial_price, shipping_extra_fees


class ProductsList(View):
    """ Display List of Products with Pagination & Filter Options """
    def get(self, request):
        # Query
        search_q = request.GET.get("search", None)
        category_q = request.GET.get("category", None)
        products_queryset = Product.objects.exclude(Q(show=False)|Q(deleted=True))
        # Filter By Search
        if search_q:
            query = Q(en_name__icontains=search_q) | Q(ar_name__icontains=search_q) | Q(fr_name__icontains=search_q)
            products_queryset = products_queryset.filter(query)
        # Filter By Category
        if category_q:
            products_queryset = products_queryset.filter(category__slug=category_q)
        # Randomize results
        final_products = list(products_queryset)
        shuffle(final_products)
        # Pagination
        products   = Paginator(final_products, 20)
        page_number = request.GET.get('page', '1')
        current_page = products.get_page(page_number)
        # Finish
        context = {
            'products':products,
            'page_number':int(page_number),
            'current_page':current_page,
            }
        return render(request, 'products/list.html', context)


class ProductDetail(View):
    def get(self, request, product_slug):
        # Query
        query = Product.objects.exclude(Q(show=False)|Q(deleted=True))
        product = get_object_or_404(query, slug=product_slug)
        # Shipping Calculation
        if not request.user.is_anonymous:
            initial_price = shipping_initial_price("paid", product.warehouse, request.user.member.wilaya, request.user.member.commune)
            extra_fees = shipping_extra_fees("paid", product)
            # Paid Shipping Price
            shipping_price = initial_price + extra_fees
        else:
            shipping_price = None
        context = {
            'product':product,
            'shipping_price':shipping_price,
        }
        return render(request, 'products/detail.html', context)

    def add_to_cart(self, request, item_id, shipping, quantity, message):
        quantity_int = int(quantity)
        cart = request.session.get('cart', {})
        cart[item_id] = [shipping, abs(quantity_int), message]
        request.session['cart'] = cart
        
    def post(self, request, product_slug):
        # Query
        query = Product.objects.exclude(Q(stock=0)|Q(show=False)|Q(deleted=True))
        product = get_object_or_404(query, slug=product_slug)
        next_ = request.POST['next']
        quantity = request.POST['quantity']
        shipping = request.POST['shipping']
        message = request.POST['orderDetails']
        # Check Quantity
        if int(quantity) > product.stock:
            messages.error(request, _("The quantity you wish to purchase is greater than the quantity in stock"))
            return redirect(reverse('detail_product', args=[product_slug]))
        # Add to Cart
        self.add_to_cart(request, product.id, shipping, quantity, message)
        # Success
        messages.success(request, _('Item has been added to cart'))
        return redirect(next_)
        