# Generated by Django 4.2.4 on 2023-11-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_email_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]
