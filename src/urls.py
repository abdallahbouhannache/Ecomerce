# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# Membership
from membership.views.authentication import Register
# Home
from home.views.products import ProductsList
from home.views.payment import Success, Fail
from home.api.calculation import PaidShippingAPI
# Shipping
from shipping.api.wilaya_handler import GetCommunes
# Source
from src.languages import i18n_switcher


urlpatterns = [
    # Control
    path('elidara/', admin.site.urls),
    path('admin-dashboard/warehouse/', include('shipping.admin_urls')),
    path('i18n_switcher/<str:prefix>/', i18n_switcher, name="i18n_switcher"),
    path('', ProductsList.as_view(), name='index'), 
    path('emergency/', include('maintenance_mode.urls')),
    # Urls
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', Register.as_view(), name="create_account"),
    path('site/', include('home.urls')),
    path('page/', include('page.urls')),
    path('member/', include('membership.urls')),
    path('shop/', include('store.urls')),
    path('success/', Success.as_view(), name="success-payment"),
    path('fail/', Fail.as_view(), name="fail-payment"),
    # API
    path('api/v1/paid_shipping_price/<str:product_slug>/<str:mode>/', PaidShippingAPI.as_view(), name="paid_shipping_price"),
    path('api/v1/wilaya/<str:wilaya_id>/', GetCommunes.as_view(), name="get_commune"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




