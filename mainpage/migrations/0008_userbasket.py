# Generated by Django 3.0.6 on 2020-06-21 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainpage', '0007_auto_20200615_0727'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBasket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(to='mainpage.Item')),
            ],
        ),
    ]