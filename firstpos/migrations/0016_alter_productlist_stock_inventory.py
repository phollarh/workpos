# Generated by Django 5.0.3 on 2024-04-19 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstpos', '0015_alter_payment_amount_tenderd_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlist',
            name='stock_inventory',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=50, null=True),
        ),
    ]
