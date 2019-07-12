# Generated by Django 2.2.2 on 2019-07-10 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20190710_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='others', max_length=2046),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
