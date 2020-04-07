from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from user_web_interface.sticker_game_control import new_game, game_position, player_on_turn, remove_cards, delete_game, print_all_games, get_game_information
from user_web_interface.forms import GameForm
import re

def home(request):
    game_id = new_game()
    game_information = get_game_information(game_id)
    form = GameForm(game_information['position'])
    return render(request, 'home.html', {'form':form, 'current_player':game_information['player'], 'game_id':game_id})

def make_a_move(request, game_id):
    game_information = get_game_information(game_id)
    form = GameForm(game_information['position'], request.POST)
    if form.is_valid():
         removal_message = remove_cards(list(request.POST), game_id)
         if re.search('Game over', removal_message):
             return HttpResponseRedirect(reverse('end_game', args=(game_id,)))
         else:
             return HttpResponseRedirect(reverse('view_game', args=(game_id,)))
    else:
        return render(request, 'home.html', {'form':form, 'current_player':game_information['player'], 'game_id':game_id})
    
def view_game(request, game_id):
    game_information = get_game_information(game_id)
    form = GameForm(game_information['position'])
    return render(request, 'home.html', {'form':form, 'current_player':game_information['player'], 'game_id':game_id})

def end_game(request, game_id):
    player = player_on_turn(game_id)
    return HttpResponse(f'Congratulations, {player}, you won! <a>Play New Game</a>')
