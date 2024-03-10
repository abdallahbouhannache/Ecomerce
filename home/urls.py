# Django
from django.urls import path
# Home
from home.views.products import ProductsList, ProductDetail
from home.views.email import Subscribe
from home.views.cart import CartView, CartDelete
from home.views.order import OrdersList, OrderDetail, OrderDelete


urlpatterns = [
    path('products/', ProductsList.as_view(), name="list_products"),
    path('products/<slug:product_slug>/', ProductDetail.as_view(), name="detail_product"),
    path('email/', Subscribe.as_view(), name="subscribe"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/delete/', CartDelete.as_view(), name="cart-delete"),
    path('orders/', OrdersList.as_view(), name="orders-list"),
    path('orders/<str:order_id>/', OrderDetail.as_view(), name="order-detail"),
    path('orders/<str:order_id>/delete/', OrderDelete.as_view(), name="order-delete"),
    
]