from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cart(models.Model):
    idcart = models.AutoField(db_column='idCart', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart'


class CartDetails(models.Model):
    idcart_details = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    shop = models.ForeignKey('Shop', models.DO_NOTHING)
    quantity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'cart_details'


class Discount(models.Model):
    iddiscount = models.AutoField(primary_key=True)
    percentage = models.FloatField()
    quantity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'discount'


class DiscountDetails(models.Model):
    iddiscount_details = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    discount = models.ForeignKey(Discount, models.DO_NOTHING)
    shop = models.ForeignKey('Shop', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'discount_details'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Payment(models.Model):
    idpayment = models.AutoField(db_column='idPayment', primary_key=True)  # Field name made lowercase.
    invoice = models.ForeignKey(Cart, models.DO_NOTHING)
    amount = models.FloatField()
    courier_boy = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'payment'


class Product(models.Model):
    idproduct = models.AutoField(primary_key=True)
    productname = models.CharField(db_column='ProductName', max_length=45)  # Field name made lowercase.
    price = models.FloatField(db_column='Price')  # Field name made lowercase.
    image_url = models.CharField(max_length=2046)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Shop(models.Model):
    idshop = models.AutoField(primary_key=True)
    owner = models.ForeignKey('User', models.DO_NOTHING, unique=True)
    location = models.CharField(max_length=45)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'shop'


class ShopOwner(models.Model):
    idshopowner = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=45)  # Field name made lowercase.
    mobile_number = models.CharField(db_column='Mobile_number', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    email_id = models.CharField(db_column='Email_id', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'shop_owner'


class ShopStorage(models.Model):
    idshop_storage = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'shop_storage'


class Shoplog(models.Model):
    idshoplog = models.AutoField(db_column='idshopLog', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField()
    product = models.ForeignKey(Product, models.DO_NOTHING)
    shop = models.ForeignKey(Shop, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'shoplog'


class User(models.Model):
    iduser = models.AutoField(db_column='idUser', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=45)  # Field name made lowercase.
    birthyear = models.DateField(db_column='Birthyear')  # Field name made lowercase.
    mobile_number = models.CharField(db_column='Mobile_number', unique=True, max_length=45, blank=True, null=True)  # Field name madeowercase.
    email_id = models.CharField(db_column='Email_id', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    profession = models.CharField(db_column='Profession', max_length=45, blank=True, null=True)  # Field namemade lowercase.
    bkash_account_no = models.CharField(db_column='bkash account_no', max_length=45, blank=True, null=True)  #Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'user'