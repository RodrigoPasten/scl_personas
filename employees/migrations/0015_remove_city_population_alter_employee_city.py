# Generated by Django 5.2.1 on 2025-06-10 16:58

import django.db.models.deletion
import smart_selects.db_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0014_educationlevel_region_alter_employee_marital_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='population',
        ),
        migrations.AlterField(
            model_name='employee',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='region', chained_model_field='region', on_delete=django.db.models.deletion.CASCADE, to='employees.city'),
        ),
    ]
