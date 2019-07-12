from django.contrib import admin
from .models import User
from .models import Shop
from .models import Product


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('iduser', 'name', 'address')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('idshop', 'name', 'owner_id', 'location')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('idproduct', 'productname', 'price', 'image' , 'rating')


admin.site.register(User, UserAdmin)

admin.site.register(Shop, ShopAdmin)

admin.site.register(Product, ProductAdmin)
