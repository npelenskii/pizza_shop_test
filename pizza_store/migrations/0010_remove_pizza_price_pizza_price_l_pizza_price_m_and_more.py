# Generated by Django 4.0.3 on 2022-06-15 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_store', '0009_pizza_ready_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='price',
        ),
        migrations.AddField(
            model_name='pizza',
            name='price_l',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='price_m',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pizza',
            name='price_s',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
