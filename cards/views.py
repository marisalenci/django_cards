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
        game.turn = game.players.first()
        game.save()
        players = game.players.all()
        card_groups = game.deal()
        for i in range(4):
            hand, created = Hand.objects.get_or_create(
                user=players[i])
            print(players[i])
            hand.cards.clear()
            for card in card_groups[i]:
                hand.cards.add(card)
            hand.save()
        return redirect(reverse('play-game', 
            kwargs={'game_id':game.id}))
    return render(request, 'create_game.html', context)

def play_game(request, game_id):
    game = Game.objects.get(id=game_id)
    players = game.players.all()
    context = {
        'game': game,
        'hand': Hand.objects.get(
            user=request.user),
        'players': players,
    }
    return render(request, 'play_game.html', context)

def play_card(request, game_id, card_id):
    game = Game.objects.get(id=game_id)
    card = Card.objects.get(id=card_id)
    if game.cards.count() == 4:
        game.cards.clear()
    game.cards.add(card)
    game.next_turn()
    game.save()
    hand = Hand.objects.get(user=request.user)
    hand.cards.remove(card)
    hand.save()
    game.autoplay()
    game.autoplay()
    game.autoplay()
    context = {
        'card': card,
        'game': game,
        'hand': hand,
        'players': game.players.all(),
    }
    return redirect(reverse('play-game', 
            kwargs={'game_id':game.id}))


