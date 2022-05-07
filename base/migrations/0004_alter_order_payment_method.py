# Generated by Django 4.0.4 on 2022-04-30 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_order_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('CASH', 'CASH'), ('CARD', 'CARD')], max_length=4, null=True),
        ),
    ]