from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'shopDB'


urlpatterns = [
    path('', views.login_view_s, name='login_shop'),
    path('user/', views.login_success_view, name='shop_user'),
    path('shop_products/', views.All_products_view, name='shop_products'),
    path('logout/', views.logout_view, name='shop_logout'),
    #added by shawon
    #url(r'^$',views.login_view , name ="list") ,
    url(r'(?P<slug>[\w-]+)/$',views.product_detail , name ="details")
]


#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)