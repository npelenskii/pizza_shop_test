# Generated by Django 4.0.3 on 2022-06-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_store', '0005_rename_done_at_at_order_done_at_order_order_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='ingradients',
            field=models.ManyToManyField(blank=True, to='pizza_store.ingradient'),
        ),
        migrations.AlterField(
            model_name='pizza',
            name='tags',
            field=models.ManyToManyField(blank=True, to='pizza_store.tag'),
        ),
    ]
