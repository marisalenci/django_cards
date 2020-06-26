from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Card, Hand, Game

def home(request):
    return render(request, 'home.html')

def create_game(request):
    if request.method == 'GET':
        player = request.user
        game = Game.objects.create()
        game.players.add(player)
        game.save()
        context = {
            'game': game,
            'player': player,
            'other_players': User.objects.all(),
        }
    elif request.method == 'POST':
        game = Game.objects.last()
        for player in ['Player 1', 'Player 2', 'Player 3']:
            player_id = request.POST.get(player)
            game.players.add(player_id)
        game.save()
        return redirect(reverse('play-game', 
            kwargs={'game_id':game.id}))
    return render(request, 'create_game.html', context)

def play_game(request, game_id):
    game = Game.objects.get(id=game_id)
    players = game.players.all()
    card_groups = game.deal()
    for i in range(4):
        hand, created = Hand.objects.get_or_create(
            user=players[i])
        hand.cards.clear()
        for card in card_groups[i]:
            hand.cards.add(card)
        hand.save()
    context = {
        'game': game,
        'hand': Hand.objects.get(
            user=request.user),
        'players': players,
    }
    return render(request, 'play_game.html', context)
