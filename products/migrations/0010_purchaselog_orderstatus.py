# Generated by Django 2.2.2 on 2019-09-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaselog',
            name='orderStatus',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Done')], default=0, max_length=1),
        ),
    ]
