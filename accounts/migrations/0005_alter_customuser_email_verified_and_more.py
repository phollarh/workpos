# Generated by Django 4.2.4 on 2023-11-08 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
