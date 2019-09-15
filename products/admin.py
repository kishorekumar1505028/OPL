from django.contrib import admin
from .models import User
from .models import Shop
from .models import Product
from .models import ShopProduct
from .models import CategoryTag
from .models import SuperCategory
from .models import TopCategory
from .models import PurchaseLog
from .models import Profile


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')

class CategoryTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'tag')


class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'superCategory')


class TopCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'topCategory')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'old_price', 'price', 'image', 'rating')


class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'quantity')


class PurchaseLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'product', 'user', 'quantity', 'orderStatus')


admin.site.register(Shop, ShopAdmin)

admin.site.register(CategoryTag, CategoryTagAdmin)

admin.site.register(SuperCategory, SuperCategoryAdmin)

admin.site.register(TopCategory, TopCategoryAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(ShopProduct, ShopProductAdmin)

admin.site.register(PurchaseLog, PurchaseLogAdmin)
