# Generated by Django 3.0.6 on 2020-06-15 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0006_auto_20200615_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Картинка основна'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_three',
            field=models.ImageField(upload_to='', verbose_name='Картинка - 3'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image_two',
            field=models.ImageField(upload_to='', verbose_name='Картинка - 2'),
        ),
    ]