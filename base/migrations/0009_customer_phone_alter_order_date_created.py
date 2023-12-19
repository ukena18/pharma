# Generated by Django 4.0.4 on 2022-04-15 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_order_who_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.CharField(blank=True, choices=[('CASH', 'CASH'), ('CARD', 'CARD')], default='CASH', max_length=4, null=True),
        ),
    ]