from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    url('login_user/', views.login_user, name='login_user'),
    url('register_user/', views.register_user, name='register_user'),
    url('add_product/', views.add_product, name='add_product'),
    url('logout_user/', views.logout_user, name='logout_user'),
    url('cart_details/', views.cart_details, name='cart_details'),
    url('order_request_details/', views.order_request_details, name='order_request_details'),
    url('wishlist_details/', views.wishlist_details, name='wishlist_details'),
    url('checkout_details/', views.checkout_details, name='checkout_details'),
    url(r'^advanced_search/(?P<category>[\w .@+&-]+)/$', views.advanced_search, name='advanced_search'),
    url(r'^advanced_search/(?P<category>[\w .@+&-]+)/ajax/price_filter/$', views.ajax_price_filter, name='ajax_price_filter'),

]

