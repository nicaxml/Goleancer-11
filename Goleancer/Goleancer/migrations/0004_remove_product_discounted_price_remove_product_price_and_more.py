# Generated by Django 5.1.4 on 2024-12-12 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Goleancer', '0003_product_service_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discounted_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='service_offer',
        ),
    ]
