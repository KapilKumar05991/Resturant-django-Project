# Generated by Django 5.1.4 on 2024-12-25 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base_App', '0003_cart_cartitem_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Base_App.dish'),
        ),
    ]
