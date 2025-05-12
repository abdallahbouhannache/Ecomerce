# Python
from django.utils import timezone
# Django
from django.views import View
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Home
from home.models import Bill
from home.utils import return_items_to_store
from home.templatetags.allow_delete import check_delete_deadline


def return_to_stock(bill):
    """
    when a bill is deleted, then return items to stock
    """
    items = bill.orders.all()
    if items:
        with transaction.atomic():
            # Model (Order)
            for item in items:
                item.product.stock += item.quantity
                item.product.save()
        return 1
    return 0


class OrdersList(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Show Bills to users as Orders
        orders = Bill.objects.exclude(status='Canceled').filter(user=request.user)
        context = {
            "orders":orders,
        }
        return render(request, 'history/orders_list.html', context)



class OrderDetail(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id):
        # Show Bills to users as Orders
        orders = Bill.objects.exclude(status='Canceled').filter(user=request.user)
        order = get_object_or_404(orders, id=order_id)
        # Check if the order is not paid yet
        if not order.is_paid:
            # Check if it's expired
            if timezone.now() > order.auto_delete_at:
                # Return items to stock
                apply_return = return_to_stock(order)
                # Delete order
                if apply_return == 1:
                    order.delete()
        context = {
            "order":order,
        }
        return render(request, 'history/order_detail.html', context)


class OrderDelete(View):

    def get(self, request, order_id):
        query = Bill.objects.exclude(status="Canceled")
        bill  = get_object_or_404(query, user=request.user, id=order_id)
        # Don't delete after 24 hrs
        allow_delete = check_delete_deadline(bill.auto_delete_at)
        if not allow_delete:
            return redirect(reverse('orders-list'))
        # Return objects to stock
        return_items_to_store(bill)
        if bill.status == "Canceled":
            messages.success(request, _("The order Nº{} has been canceled, you will be refunded if you paid using CIB").format(order_id))
        else:
            messages.error(request, _("The order Nº{} can not canceled, please contact support").format(order_id))
        return redirect(reverse('orders-list'))

