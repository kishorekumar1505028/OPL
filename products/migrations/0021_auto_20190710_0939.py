# Generated by Django 2.2.2 on 2019-07-10 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_product_image_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'managed': False},
        ),
    ]