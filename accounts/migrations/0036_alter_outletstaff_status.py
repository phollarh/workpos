# Generated by Django 4.2.4 on 2023-12-14 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_alter_outletstaff_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outletstaff',
            name='status',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Supervisor', 'Supervisor'), ('Staff', 'Staff')], default='staff', max_length=100),
        ),
    ]
