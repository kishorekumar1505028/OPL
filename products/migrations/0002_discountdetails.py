# Generated by Django 2.2.2 on 2019-06-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountDetails',
            fields=[
                ('iddiscount_details', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'discount_details',
                'managed': False,
            },
        ),
    ]
