# Django
from django.urls import path
# Shipping
from shipping.views.administration import AdminWilayaList, AdminCommunesList

urlpatterns = [
    path('<str:warehouse_id>/', AdminWilayaList.as_view(), name="admin_wilaya_list"),
    path('<str:warehouse_id>/<str:wilaya_id>/', AdminCommunesList.as_view(), name="admin_communes_list"),
]