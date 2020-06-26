from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Card, Hand, Game

def home(request):
    return render(request, 'home.html')

def game(request):
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
        return redirect('home')
    return render(request, 'game.html', context)
