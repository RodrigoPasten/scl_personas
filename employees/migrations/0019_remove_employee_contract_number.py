# Generated by Django 5.2.1 on 2025-06-10 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0018_employee_boss_workplace_adc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='contract_number',
        ),
    ]
