# Generated by Django 5.1.1 on 2024-09-09 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='modifiers',
            field=models.ManyToManyField(related_name='order_items', to='menu.modifier'),
        ),
    ]
