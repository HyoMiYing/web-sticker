from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from user_web_interface.sticker_game_control import WebStickerGameManager
from user_web_interface.forms import GameForm, CreateNewGameForm
import re

game_manager = WebStickerGameManager()

def home(request):
    return render(request, 'home.html', {'form': CreateNewGameForm()})

def create_new_game(request):
    form = CreateNewGameForm(request.POST)
    if form.is_valid():
        game_id = game_manager.instantiate_new_WebStickerGame(form.cleaned_data)
    else:
        raise Http404('Something went wrong. Game was not created.')
    return redirect('view_round', game_id)

def make_a_move(request, game_id):
    round_information = game_manager.get_round_information(game_id)
    if not round_information:
        raise Http404("Game does not exist anymore")
    form = GameForm(round_information['position'], request.POST)
    if form.is_valid():
         removal_message = game_manager.remove_cards(list(request.POST), game_id)
         if re.search('Game over', removal_message):
             return HttpResponseRedirect(reverse('end_round', args=(game_id,)))
         else:
             return HttpResponseRedirect(reverse('view_round', args=(game_id,)))
    else:
        return render(request, 'home.html', {'form':form, 'current_player':round_information['player'], 'game_id':game_id})
    
def view_round(request, game_id):
    round_information = game_manager.get_round_information(game_id)
    # In case the round ended
    if round_information == False:
        return redirect('end_round', game_id)
    elif round_information['position'] == [0, 0, 0, 0]:
        return redirect('end_round', game_id)
    form = GameForm(round_information['position'])
    return render(request, 'game.html', {'form':form, 'current_player':round_information['player'], 'game_id':game_id, 'player_number':round_information['player_number']})

def end_round(request, game_id):
    game_status = game_manager.get_game_status(game_id)
    if 'Game over' in game_status:
        return HttpResponseRedirect(reverse('end_game', args=(game_id,)))
    round_winner = game_manager.get_winner(game_id)
    number_of_played_rounds = game_status['number_of_played_rounds']
    number_of_all_rounds = game_status['number_of_all_rounds']
    return render(request, 'end_round.html', {'round_winner': round_winner, 'number_of_played_rounds': number_of_played_rounds, 'number_of_all_rounds': number_of_all_rounds, 'game_id': game_id})

def end_game(request, game_id):
    game_status = game_manager.get_game_status(game_id)
    if game_status['Game over']:
        if 'winner' in game_status:
            context = {'winner': game_status['winner']}
        else:
            context = {'tie': 'It\'s a tie!'}
        context['number_of_played_rounds'] = game_status['number_of_played_rounds']
        context['player1'] = game_status['player1']
        context['player2'] = game_status['player2']
        if game_status['player1_wins']: 
            context['player1_wins'] = game_status['player1_wins']
        if game_status['player2_wins']: 
            context['player2_wins'] = game_status['player2_wins']
    else:
        return HttpResponseRedirect(reverse('view_round', args=(game_id,)))
    return render(request, 'end.html', context)

def admin_page(request):
    return render(request, 'admin.html', {'admin_data': game_manager.get_admin_data()})

def handler404(request):
    return render(request, '404.html', status=404)
