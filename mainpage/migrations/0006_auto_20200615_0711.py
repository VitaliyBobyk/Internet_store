# Generated by Django 3.0.6 on 2020-06-15 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0005_auto_20200613_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image_three',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Картинка'),
        ),
        migrations.AddField(
            model_name='item',
            name='image_two',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Картинка'),
        ),
    ]
