# Generated by Django 4.0.4 on 2022-04-15 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='who_paid',
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.customer'),
        ),
    ]
