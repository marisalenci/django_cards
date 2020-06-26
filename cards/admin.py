from django.contrib import admin

from cards.models import Card, Hand, Game

admin.site.register(Card)
admin.site.register(Hand)
admin.site.register(Game)