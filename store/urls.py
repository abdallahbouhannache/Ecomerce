# Django
from django.urls import path
# Store
from store.views.user_store import (
    AddNewStore, MerchantStoreIndex,
    MerchantStoreList,
    MerchantStoreAdd,
    MerchantStoreUpdate,
    MerchantStoreDelete,
)


urlpatterns = [
    path('add-store/', AddNewStore.as_view(), name="submit_new_store"),
    path('mystores/', MerchantStoreIndex.as_view(), name="merchant_store_index"),
    path('mystores/<slug:store_slug>/', MerchantStoreList.as_view(), name="merchant_store_list"),
    path('mystores/<slug:store_slug>/add/', MerchantStoreAdd.as_view(), name="store_add_product"),
    path('mystores/<slug:store_slug>/<slug:product_slug>/change/', MerchantStoreUpdate.as_view(), name="store_update_product"),
    path('mystores/<slug:store_slug>/<slug:product_slug>/delete/', MerchantStoreDelete.as_view(), name="store_delete_product"),
]