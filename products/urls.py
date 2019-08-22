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
    url('logout_user/', views.logout_user, name='logout_user'),
    url(r'^advanced_search/(?P<category>[\w .@+&-]+)/$', views.advanced_search, name='advanced_search'),
    url(r'^advanced_search/(?P<category>[\w .@+&-]+)/ajax/price_filter/$', views.ajax_price_filter, name='ajax_price_filter'),

]

