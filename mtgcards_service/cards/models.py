from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    card_name = models.CharField(max_length=200)
    path = models.CharField(max_length=100)


class Purchases(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    user = models.OneToOneField(User)
