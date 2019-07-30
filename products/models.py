from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)  # Field name made lowercase.
    address = models.CharField(max_length=45)  # Field name made lowercase.
    birth_year = models.DateField()  # Field name made lowercase.
    mobile_number = models.CharField(unique=True, max_length=45, blank=True,
                                     null=True)  # Field name madeowercase.
    email = models.CharField(unique=True, max_length=45)  # Field name made lowercase.
    profession = models.CharField(max_length=45, blank=True, null=True)  # Field namemade lowercase.
    bkash_account_no = models.CharField(max_length=45)  # Field renamed to remove unsuitable characters.

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_profile'


# update profile on change in User
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Product(models.Model):
    name = models.CharField(max_length=45)  # Field name made lowercase.
    price = models.FloatField()  # Field name made lowercase.
    category = models.CharField(default='others' , max_length=45)
    rating = models.IntegerField(default='0')
    image = models.ImageField(max_length=100, blank=True, null=True, upload_to='img')

    class Meta:
        db_table = 'product'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart'


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'cart_products'


class ProductDiscount(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0)

    class Meta:
        db_table = 'discount'


class UserDiscount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.ForeignKey(ProductDiscount, on_delete=models.CASCADE)
    shop = models.ForeignKey('Shop', models.DO_NOTHING)

    class Meta:
        db_table = 'discount_for_user'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        db_table = 'payment'


class Shop(models.Model):
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)

    class Meta:
        db_table = 'shop'


class ShopProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'shop_storage'


class PurchaseLog(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        db_table = 'purchase_log'
