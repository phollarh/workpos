# Generated by Django 4.2.4 on 2023-12-26 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstpos', '0010_alter_productlist_stock_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlist',
            name='stock_inventory',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
