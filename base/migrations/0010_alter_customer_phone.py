# Generated by Django 4.0.4 on 2022-04-15 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_customer_phone_alter_order_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
