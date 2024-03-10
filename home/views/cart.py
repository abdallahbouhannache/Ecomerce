# Django
from django.utils import timezone
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Home
from home.utils import shipping_initial_price, shipping_extra_fees, randomize_order_id
from home.models import Product, Order, Bill
from home.forms import OrderForm
from home.payments import initilize_create_satim_bill, create_satim_bill

class CartView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def items_only_price(self, items):
        """
        Calculate the price of items only
        """
        total = 0
        if items:
            for item in items:
                total += item['product'].sell_price() * item['qty']
        return float(total)

    def one_product_shipping_price(self, request, product):
        # Shipping Calculation
        initial_price = shipping_initial_price("paid", product.warehouse, request.user.member.wilaya, request.user.member.commune)
        extra_fees = shipping_extra_fees("paid", product)
        # Paid Shipping Price
        return initial_price + extra_fees

    def shipping_only_price(self, request, items):
        """
        Calculate the price of shipping only
        """
        total = 0
        for item in items:
            product = item['product']
            if item['shipping'] == 'paid':
                shipping_price = self.one_product_shipping_price(request, product)
                total += shipping_price
        return total

    def bill_total_price(self, request, items):
        """
        Calculate total price of bill, including shipping
        """
        return self.items_only_price(items) + self.shipping_only_price(request, items)

    def get_cart_items(self, request):
        """
        Return None or List of dict like:
        {id, product, qty, msg}
        """
        # Init Cart
        items_ = request.session.get('cart', None)
        if items_ is not None:
            items = [
                {
                    'id':item,
                    'product':Product.objects.get(id=item),
                    'shipping':items_[item][0],
                    'qty':items_[item][1],
                    'msg':items_[item][2],
                    'paid_shipping':self.one_product_shipping_price(request, Product.objects.get(id=item))
                } for item in items_]
        else:
            items = None
        return items

    def get(self, request):
        """
        Display Cart with current items on it
        """
        # Init Cart
        items = self.get_cart_items(request)
        if items is None:
            messages.warning(request, _("There are no items in your cart, please choose items first"))
            return redirect('index') 
        data = {
            'first_name':request.user.first_name,
            'last_name':request.user.last_name,
            'phone_number':request.user.member.phone_number,
            'address':request.user.member.address,
            'wilaya':request.user.member.get_wilaya_display,
            'commune':request.user.member.get_commune_display,
            'zip_code':request.user.member.zip_code,
        }
        form = OrderForm(initial=data)
        # Response
        context = {
            "data":data,
            "form":form,
            "items":items,
            "total_shipping": self.shipping_only_price(request, items),
            "total": self.bill_total_price(request, items),
        }
        return render(request, 'cart.html', context)

    @staticmethod
    def reduce_quantity(item, quantity):
        """ Reduce Quantity """
        item.stock = item.stock - quantity
        item.save()

    def populate_orders(self, request, items):
        """ Create Orders from items in the cart """
        orders = []
        for item in items:
            # Decrease Stock
            if item['qty'] > item['product'].stock:
                messages.error(request, _("The quantity you wish to purchase for {} is greater than the quantity in stock").format(item['product'].get_name()))
                return redirect('cart')
            self.reduce_quantity(item['product'], item['qty'])
            # Create the Order
            new_order = Order(
                order_date       = timezone.now(),
                product          = item['product'],
                quantity         = item['qty'],
                individual_price = item['product'].sell_price(),
                message          = item['msg'],
            )
            new_order.save()
            # Append to orders List
            orders.append(new_order)
        return orders

    def post(self, request):
        """
        Submit a new Bill
        """
        # Init Cart
        items = self.get_cart_items(request)
        user = request.user
        # Check when a user submit a blank order
        if not items:
            messages.warning(request, _("Please choose the products you wish to purchase first"))
            return redirect('index')
        # Validate Data
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Start Processing
            with transaction.atomic():
                # Products in Cart
                orders = self.populate_orders(request, items)
                # When finish add all to the createed bill
                products_price = self.items_only_price(items)
                shipping_price = self.shipping_only_price(request, items)
                # Handle Payment Methods
                payment_option = data['payment_method']
                # Initilize Bill data
                bill_data = {
                    'key':randomize_order_id(),
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'phone_number':user.member.phone_number,
                    'address':user.member.address,
                    'wilaya':user.member.wilaya,
                    'commune':user.member.commune,
                    'zip_code':user.member.zip_code,
                }
                # Payment By Eddahabia
                if payment_option == "direct":
                    # Calculate Total of bill for SATIM
                    satim_payment_total = int((products_price + shipping_price) * 100) # To centime because they accept centime
                    # Return response and status code
                    status_code, response = initilize_create_satim_bill(key=bill_data['key'], amount=satim_payment_total, description=f"{bill_data['first_name']} {bill_data['last_name']} {bill_data['phone_number']}")
                    # Create SATIM Bill
                    new_bill = create_satim_bill(
                        user=request.user,
                        key=bill_data['key'],
                        form_data=bill_data,
                        satim_response_data=response,
                        products_price=products_price,
                        shipping_price=shipping_price,
                        orders=orders
                    )
                    redirect_external = True
                elif payment_option == "cash":
                    new_bill = Bill(
                        key            = bill_data['key'],
                        first_name     = bill_data['first_name'],
                        last_name      = bill_data['last_name'],
                        phone_number   = bill_data['phone_number'],
                        address        = bill_data['address'],
                        wilaya         = bill_data['wilaya'],
                        commune        = bill_data['commune'],
                        zip_code       = bill_data['zip_code'],
                        user           = request.user,
                        products_price = products_price,
                        shipping_price = shipping_price,
                        payment_option = payment_option,
                        status         = "Waiting",
                        is_paid        = True
                    )
                    new_bill.save()
                    new_bill.orders.add(*orders)
                    new_bill.save()
                    redirect_external = False
            # Success
            messages.success(request, _("Bill has been created, you can track your order in My Orders page"))
            # Update Cart
            request.session['cart'] = {}
            if redirect_external:
                return redirect(new_bill.payURL)
            return redirect('orders-list')
        # When form is not valid
        context = {
            "form":form,
            "items":items,
            "total_shipping":self.shipping_only_price(request, items),
            "total":self.bill_total_price(request, items),
        }
        return render(request, 'cart.html', context)


class CartDelete(View):
    def get(self, request):
        return redirect('index')

    def post(self, request):
        """
        Delete Requested item in cart by id
        """
        item = request.POST.get("id", None)
        next_ = request.POST.get("next", 'index')
        if item is not None:
            request.session['cart'].pop(item)
            new_cart = request.session['cart']
            request.session['cart'] = new_cart
        return redirect(next_)