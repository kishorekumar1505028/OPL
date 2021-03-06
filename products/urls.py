from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    url('login_user/', views.login_user, name='login_user'),
    url('register_user/', views.register_user, name='register_user'),
    url('vendor_homepage/', views.vendor_homepage_view, name='vendor_homepage'),
    url('logout_user/', views.logout_user, name='logout_user'),
    url('cart_details/', views.cart_details, name='cart_details'),
    url('storage_details/', views.storage_details, name='storage_details'),
    url('add_product/', views.add_product, name='add_product'),
    url('order_request_details/', views.order_request_details, name='order_request_details'),
    url('purchase_history_details/', views.purchase_history_details, name='purchase_history_details'),
    url('vendor_order_details/', views.vendor_order_request_details, name='vendor_order_request_details'),
    url('vendor_sale_history_details/', views.vendor_sale_history_details, name='vendor_sale_history_details'),
    url('wishlist_details/', views.wishlist_details, name='wishlist_details'),
    url('checkout_details/', views.checkout_details, name='checkout_details'),
    url(r'^advanced_search/(?P<category>[\w .@+&-]+)/$', views.advanced_search, name='advanced_search'),
    url(r'^advanced_search/(?P<category>[\w .@+&-]+)/ajax/price_filter/$', views.ajax_price_filter, name='ajax_price_filter'),

]

