# Generated by Django 5.1.4 on 2024-12-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Goleancer', '0004_remove_product_discounted_price_remove_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
