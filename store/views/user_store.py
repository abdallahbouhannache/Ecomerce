# Django
from django.views import View
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Home
from home.models import Product
from home.forms import ProductForm
# Store
from store.models import Store
from store.decorators import only_merchant_allowed
from store.utils import filter_data
from store.forms import StoreForm


class AddNewStore(View):

    @method_decorator(only_merchant_allowed)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        next_ = request.POST.get('next', 'index')
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # Create a new store
                store = Store(**form.cleaned_data)
                store.owner = request.user
                store.save()
                # Connect Store to current user
                request.user.member.stores.add(store)
                messages.success(request, _("Store has been created, we will review your request within 72 hours"))
        else:
            # Display errors
            template = ""
            for e in form.errors.values():
                template += f"{e.as_text()} "
            messages.error(request, template)
        return redirect(next_)




class MerchantStoreIndex(View):

    @method_decorator(only_merchant_allowed)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        stores = request.user.member.stores.filter(active=True)
        stores_on_hold = request.user.member.stores.filter(active=False)
        add_store_form = StoreForm()

        context = {
            "stores":stores,
            "stores_on_hold":stores_on_hold,
            "add_store_form":add_store_form,
        }
        return render(request, "store/index.html", context)


class MerchantStoreList(View):

    @method_decorator(only_merchant_allowed)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, store_slug):
        stores = request.user.member.stores.filter(active=True)
        stores_on_hold = request.user.member.stores.filter(active=False)
        active_store_products = filter_data(request, Product.objects.filter(store__slug=store_slug))
        add_store_form = StoreForm()

        context = {
            "stores":stores,
            "stores_on_hold":stores_on_hold,
            "active_store_products":active_store_products,
            "add_store_form":add_store_form,
            "store_slug":store_slug,
        }
        return render(request, "store/list.html", context)



class MerchantStoreAdd(View):

    @method_decorator(only_merchant_allowed)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, store_slug):
        store = get_object_or_404(Store, slug=store_slug)
        add_product_form = ProductForm()

        context = {
            "mode":"add",
            "add_product_form":add_product_form,
            "store":store,
            "store_slug":store_slug,
        }
        return render(request, "store/detail.html", context)


    def post(self, request, store_slug):
        store = get_object_or_404(Store, slug=store_slug)
        add_product_form = ProductForm(request.POST, request.FILES)
        # Hadle Adding Products
        if add_product_form.is_valid():
            # Connect with current store
            add_product_form.cleaned_data['store'] = store
            # Save Instance
            add_product_form.create(add_product_form.cleaned_data)
            # Return Success
            messages.success(request, "The product has been added, pending review")
            return redirect(reverse('merchant_store_list', args=[store_slug]))
        else:
            # Return Fail
            messages.error(request, "Please fix highlighted errors")
            context = {
                "add_product_form":add_product_form,
                "store":store,
                "store_slug":store_slug,
                "mode":"add",
            }
            return render(request, "store/detail.html", context)


class MerchantStoreUpdate(View):

    @method_decorator(only_merchant_allowed)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, store_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        add_product_form = ProductForm(instance=product)

        context = {
            "mode":"update",
            "add_product_form":add_product_form,
            "product":product,
            "store":product.store,
            "store_slug":store_slug,
        }
        return render(request, "store/detail.html", context)


    def post(self, request, store_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        add_product_form = ProductForm(request.POST, request.FILES, instance=product)
        # Hadle Adding Products
        if add_product_form.is_valid():
            # Save Instance
            add_product_form.update(product)
            # Return Success
            messages.success(request, "The product has been updated, pending review")
            return redirect(reverse('merchant_store_list', args=[store_slug]))
        else:
            # Return Fail
            messages.error(request, "Please fix highlighted errors")
            context = {
                "mode":"update",
                "add_product_form":add_product_form,
                "product":product,
                "store":product.store,
                "store_slug":store_slug,
            }
            return render(request, "store/detail.html", context)


class MerchantStoreDelete(View):

    @method_decorator(only_merchant_allowed)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, store_slug, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        product.deleted = True
        product.save()
        messages.success(request, _("Product has been disabled"))
        return redirect(reverse('merchant_store_list', args=[store_slug]))
