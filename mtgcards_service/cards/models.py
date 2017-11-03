from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    name = models.CharField(max_length=200)
    local_path = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Purchases(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.card)
