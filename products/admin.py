from django.contrib import admin
from .models import User
from .models import Shop
from .models import Product
from .models import ShopProduct


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image', 'rating')


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'quantity')


admin.site.register(Shop, ShopAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(ShopProduct, ShopProductAdmin)
