from django.db import models
from django.contrib.auth.models import User
from mainpage.models import Item


class UserBasket(models.Model):
    current_user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
