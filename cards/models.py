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

    def get_display_name(self):
        if self.number == 14:
            value = 'A'
        elif self.number == 13:
            value = 'K'
        elif self.number == 12:
            value = 'Q'
        elif self.number == 11:
            value = 'J'
        else:
            value = self.number
        return value

class Hand(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, blank=True)

    def __str__(self):
        return self.user.username + "'s Hand"

class Game(models.Model):

    players = models.ManyToManyField(User, blank=True)
    cards = models.ManyToManyField(Card, blank=True)

    def shuffle(self):
        cards = Card.objects.all().order_by('?')
        return cards

    def deal(self):
        cards = self.shuffle()
        group_1 = cards[:13]
        group_2 = cards[13:26]
        group_3 = cards[26:39]
        group_4 = cards[39:52]
        return group_1, group_2, group_3, group_4