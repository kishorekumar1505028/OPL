from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.initial_page, name='initial_page'),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),
    path('user_login/', views.user_login, name='user_login'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
]

