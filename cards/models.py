from django.contrib.auth.models import User
from django.db import models


class Card(models.Model):
    SUIT_CHOICES = (
        ('diamonds', 'Diamonds'),
        ('hearts', 'Hearts'),
        ('clubs', 'Clubs'),
        ('spades', 'Spades'),
    )

    number = models.IntegerField()
    suit = models.CharField(max_length=50, choices=SUIT_CHOICES)

    def __str__(self):
        if self.number == 14:
            value = 'Ace'
        elif self.number == 13:
            value = 'King'
        elif self.number == 12:
            value = 'Queen'
        elif self.number == 11:
            value = 'Jack'
        else:
            value = str(self.number)
        return value + ' of ' + self.suit

class Hand(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, blank=True)

class Game(models.Model):

    players = models.ManyToManyField(User, blank=True)
    cards = models.ManyToManyField(Card, blank=True)