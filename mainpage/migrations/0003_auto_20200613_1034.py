# Generated by Django 3.0.6 on 2020-06-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_auto_20200612_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='old_price',
            field=models.CharField(blank=True, max_length=150, verbose_name='Стара ціна'),
        ),
    ]