# Generated by Django 4.0.3 on 2022-07-12 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_store', '0016_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_list',
            field=models.ManyToManyField(blank=True, to='pizza_store.orderitem'),
        ),
    ]
