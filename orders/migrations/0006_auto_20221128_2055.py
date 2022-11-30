# Generated by Django 3.1 on 2022-11-28 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20221126_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Order Accepted', 'Order Accepted'), ('Delivered Successfully', 'Delivered Successfully'), ('Order Cancelled', 'Order Cancelled')], default='New', max_length=55),
        ),
    ]