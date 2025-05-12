# Python
from datetime import datetime
# Django
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Home
from home.models import Bill
from home.utils import return_items_to_store
from home.payments import initilize_check_satim_bill

class Success(View):

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        orderId = request.GET.get('orderId', None)
        if not orderId:
            return redirect('index')
        # Get Order from DB
        try:
            success_bill = Bill.objects.get(orderID=orderId)
        except Bill.DoesNotExist as e:
            messages.error(request, str(e))
            return redirect('index')
        # Check the bill with SATIM
        status_code, response = initilize_check_satim_bill(orderId)
        # Update failed bill with SATIM response
        success_bill.order_status = response.get('OrderStatus', None)
        success_bill.error_code = response.get('ErrorCode', None)
        success_bill.error_message = response.get('ErrorMessage', None)
        success_bill.action_code = response.get('actionCode', None)
        success_bill.action_code_description = response['params'].get("respCode_desc", None) or response.get("actionCodeDescription", None)
        success_bill.SVFE_response = response.get('SvfeResponse', None)
        success_bill.pan = response.get('Pan', None)
        success_bill.expiration = response.get('expiration', None)
        success_bill.cardholder_name = response.get('cardholderName', None)
        success_bill.amount = response.get('Amount', None)
        success_bill.deposit_amount = response.get('depositAmount', None)
        success_bill.currency_code = response.get('currency', None)
        success_bill.approval_code = response.get('approvalCode', None)
        success_bill.auth_code = response.get('authCode', None)
        success_bill.ip = response.get('Ip', None)
        success_bill.is_paid = True
        success_bill.save()
        # Update Bill informations
        context = {
            "respCode_desc" : response['params'].get("respCode_desc", None),
            "orderId": orderId,
            "orderNumber" : response.get("OrderNumber", None),
            "approvalCode" : response.get("approvalCode", None),
            "transaction_date_time" : success_bill.create_date,
            "depositAmount" : response.get("depositAmount", None),
            "pay_method" : 'Carte CIB',
        }
        return render(request, 'page/success.html', context)


class Fail(View):

    def get(self, request):
        orderId = request.GET.get('orderId', None)
        if not orderId:
            return redirect('index')
        # Get Order from DB
        try:
            failed_bill = Bill.objects.get(orderID=orderId)
        except Bill.DoesNotExist as e:
            messages.error(request, str(e))
            return redirect('index')
        # Check the bill with SATIM
        status_code, response = initilize_check_satim_bill(orderId)
        error_code = response.get('ErrorCode', None)
        error_msg  = response.get('ErrorMessage', None)
        # Update failed bill with SATIM response
        failed_bill.order_status = response.get('OrderStatus', None)
        failed_bill.error_code = response.get('ErrorCode', None)
        failed_bill.error_message = response.get('ErrorMessage', None)
        failed_bill.action_code = response.get('actionCode', None)
        failed_bill.action_code_description = response['params'].get("respCode_desc", None) or response.get("actionCodeDescription", None)
        failed_bill.SVFE_response = response.get('SvfeResponse', None)
        failed_bill.pan = response.get('Pan', None)
        failed_bill.expiration = response.get('expiration', None)
        failed_bill.cardholder_name = response.get('cardholderName', None)
        failed_bill.amount = response.get('Amount', None)
        failed_bill.deposit_amount = response.get('depositAmount', None)
        failed_bill.currency_code = response.get('currency', None)
        failed_bill.approval_code = response.get('approvalCode', None)
        failed_bill.auth_code = response.get('authCode', None)
        failed_bill.ip = response.get('Ip', None)
        failed_bill.client_id = response.get('clientId', None)
        failed_bill.binding_id = response.get('bindingId', None)
        failed_bill.save()
        # Return to store, AWARE: DON'T RETURN ITEMS WHEN BILL ALREADY CANCELED
        return_items_to_store(failed_bill)
        if response.get("respCode") == '00' and response.get("ErrorCode") == '0' and response.get("OrderStatus") == '3':
            context = {
                'error_code':error_code,
                'error_msg':error_msg,
                'action_description': "Votre transaction a été rejetée / Your transaction was rejected / تم رفض معاملتك",
            }
        else:
            context = {
                'error_code':error_code,
                'error_msg':error_msg,
                'action_description':failed_bill.action_code_description,
            }
        return render(request, 'page/fail.html', context)
