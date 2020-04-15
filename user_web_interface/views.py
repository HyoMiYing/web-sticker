from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from user_web_interface.sticker_game_control import new_game, game_position, player_on_turn, remove_cards, print_all_games, get_game_information, get_all_games_data, delete_game_after_x_seconds, delete_game, create_custom_names_for_the_game
from user_web_interface.forms import GameForm, CreateNewGameForm
import re

def home(request):
    
    return render(request, 'home.html', {'all_games_data': get_all_games_data(), 'form': CreateNewGameForm()})

def create_new_game(request):
    form = CreateNewGameForm(request.POST)
    if form.is_valid():
        game_id = new_game()
        create_custom_names_for_the_game(form.cleaned_data, game_id)
    else:
        raise Http404('Something went wrong. Game was not created.')
    return redirect('view_game', game_id)

def make_a_move(request, game_id):
    game_information = get_game_information(game_id)
    if not game_information:
        raise Http404("Game does not exist anymore")
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
    # In case the game ended
    if game_information == False:
        return redirect('end_game', game_id)
    elif game_information['position'] == [0, 0, 0, 0]:
        return redirect('end_game', game_id)
    form = GameForm(game_information['position'])
    return render(request, 'game.html', {'form':form, 'current_player':game_information['player'], 'game_id':game_id})

def end_game(request, game_id):
    player = player_on_turn(game_id)
    if player == False:
        return redirect('home')
    # delete_game(game_id)
    # delete_game_after_x_seconds(game_id, 120)
    return render(request, 'end.html', {'player' : player})

def admin_page(request):
    return render(request, 'admin.html', {'all_games_data': get_all_games_data()})

def handler404(request):
    return render(request, '404.html', status=404)
