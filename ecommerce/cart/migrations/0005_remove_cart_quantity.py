# Generated by Django 2.2.3 on 2019-07-18 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
    ]
