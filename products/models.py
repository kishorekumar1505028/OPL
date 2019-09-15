from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Profile of user """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=45, default="foo")
    last_name = models.CharField(max_length=45, default="foo")
    address = models.CharField(max_length=45)
    profession = models.CharField(max_length=45, blank=True, null=True)
    mobile_number = models.CharField(unique=True, max_length=11, blank=True, null=True)
    bkash_account_no = models.CharField(max_length=45)
    image = models.ImageField(blank=True, null=True, upload_to='img')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_profile'


# update profile on change in User
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """profile update function """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class TopCategory(models.Model):
    topCategory = models.CharField(max_length=45)

    class Meta:
        db_table = 'top_category'


class SuperCategory(models.Model):
    superCategory = models.CharField(max_length=45)

    class Meta:
        db_table = 'super_category'


class TopSuper(models.Model):
    topCategory = models.ForeignKey(TopCategory, on_delete=models.CASCADE)
    superCategory = models.ForeignKey(SuperCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'top_super'


class CategoryTag(models.Model):
    category = models.CharField(max_length=45, default="others")
    tag = models.CharField(max_length=450, default="empty")
    superCategory = models.ForeignKey(SuperCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_tag'


def product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'img/{0}/{1}'.format(instance.category.category.lower(), filename)


class Product(models.Model):
    """Product refers to the products of the site"""

    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField(default='0')
    old_price = models.FloatField(default='0')
    price = models.FloatField(default='0')
    discount = models.FloatField(default='0')
    rating = models.IntegerField(default='0')
    image = models.ImageField(max_length=1000, blank=True, null=True, upload_to=product_image_path)
    category = models.ForeignKey(CategoryTag, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'


class ProductReview(models.Model):
    """Review of product"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default='0')
    review = models.CharField(max_length=2000)

    class Meta:
        db_table = 'product_review'


class Cart(models.Model):
    """ Cart class refers to the cart of the user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'cart'


class WishList(models.Model):
    """ WishList class refers to the products user wishes to purchase"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'wish_list'


class Shop(models.Model):
    """ Shop class refers to the shops of the site"""

    name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)

    class Meta:
        db_table = 'shop'


class ShopProduct(models.Model):
    """ ShopProduct class refers to the products of the shop"""

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'shop_product'


PENDING = 0
DONE = 1
STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (DONE, 'Done'),
]


class PurchaseLog(models.Model):
    """ PurchaseLog class refers to the time and product of the user's purchase"""

    time = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    orderStatus = models.IntegerField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    class Meta:
        db_table = 'purchase_log'


@receiver(post_save, sender=PurchaseLog)
def update_product_quantity(sender, instance, created, **kwargs):
    """product quantity update function """
    if not created:
        if instance.orderStatus == DONE:
            new_quantity = Product.objects.filter(id=instance.product.id).first().quantity - instance.quantity
            Product.objects.filter(id=instance.product.id).update(quantity=new_quantity)
