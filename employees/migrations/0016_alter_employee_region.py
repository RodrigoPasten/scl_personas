# Generated by Django 5.2.1 on 2025-06-10 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0015_remove_city_population_alter_employee_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='employees.region', verbose_name='Región de origen'),
            preserve_default=False,
        ),
    ]
