# Generated by Django 4.0.4 on 2022-04-15 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_order_who_paid_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='who_paid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_requests_created', to='base.customer'),
        ),
    ]
