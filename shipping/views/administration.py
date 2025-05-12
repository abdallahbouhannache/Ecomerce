# Python
import json
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.conf import settings
# Shipping
from shipping.models import Warehouse
from shipping.utils.admin_functions import load_wilaya, update_wilaya, load_communes, update_communes

# Create your views here.

class AdminWilayaList(View):
    """
    Display list of wilaya related to a warehouse
    """
    def get(self, request, warehouse_id):
        # Open Warehouse and it's related data
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        measruing_unit, currency, warehouse_wilaya = load_wilaya(warehouse.name)
        # Render the page
        context = {
            'warehouse':warehouse,
            'measruing_unit':measruing_unit,
            'currency':currency,
            'warehouse_wilaya':warehouse_wilaya,
        }
        return render(request, "shipping/admin_wilaya_list.html", context)

    def post(self, request, warehouse_id):
        # Open Warehouse and it's related data
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        # Respect Order of wilayat
        distances = request.POST.getlist('wilaya_distance_between')
        prices    = request.POST.getlist('wilaya_initial_price')
        # Update values
        update_wilaya(distances, prices, warehouse)
        # Return success
        messages.success(request, _("You have updated wilaya settings successfuly"))
        return redirect(reverse('admin:shipping_warehouse_changelist'))


class AdminCommunesList(View):
    """
    Display list of communes related to a wilaya which is related to warehouse
    """
    def get(self, request, warehouse_id, wilaya_id):
        # Open Warehouse and it's related data
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        measruing_unit, currency, warehouse_wilaya_communes, wilaya = load_communes(warehouse.name, wilaya_id)
        # Render the page
        context = {
            'warehouse':warehouse,
            'wilaya':wilaya,
            'measruing_unit':measruing_unit,
            'currency':currency,
            'warehouse_wilaya_communes':warehouse_wilaya_communes,
        }
        return render(request, "shipping/admin_communes_list.html", context)

    def post(self, request, warehouse_id, wilaya_id):
        # Open Warehouse and it's related data
        warehouse = get_object_or_404(Warehouse, id=warehouse_id)
        # Respect Order of wilayat
        distances = request.POST.getlist('wilaya_distance_between')
        prices    = request.POST.getlist('wilaya_initial_price')
        # Update values
        update_communes(distances, prices, warehouse, wilaya_id)
        # Return success
        messages.success(request, _("You have updated wilaya settings successfuly"))
        return redirect(reverse('admin:shipping_warehouse_changelist'))