import random
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
    turn = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, 
        related_name='turns')

    def shuffle(self):
        cards = Card.objects.all().order_by('?')
        ids = list(Card.objects.values_list('id', flat=True))
        random.shuffle(ids)
        return ids

    def deal(self):
        shuffled_cards = self.shuffle()
        group_1 = Card.objects.filter(id__in=shuffled_cards[:13])
        group_2 = Card.objects.filter(id__in=shuffled_cards[13:26])
        group_3 = Card.objects.filter(id__in=shuffled_cards[26:39])
        group_4 = Card.objects.filter(id__in=shuffled_cards[39:52])
        return group_1, group_2, group_3, group_4

    def next_turn(self):
        remaining_players = self.players.filter(id__gt=self.turn.id).order_by('id')
        if remaining_players:
            self.turn = remaining_players[0]
        else:
            self.turn = self.players.order_by('id')[0]
        self.save()

    def autoplay(self):
        next_player_hand = self.turn.hand
        next_player_cards = next_player_hand.cards.all()
        card_to_play = next_player_cards.first()
        self.cards.add(card_to_play)
        next_player_hand.cards.remove(card_to_play)
        next_player_hand.save()
        self.next_turn()
