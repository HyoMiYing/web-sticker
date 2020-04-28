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
    return render(request, 'game.html', {'form':form, 'current_player':round_information['player'], 'game_id':game_id})

def end_round(request, game_id):
    game_status = game_manager.get_game_status(game_id)
    round_winner = game_manager.get_winner(game_id)
    number_of_played_rounds = game_status['number_of_played_rounds']
    number_of_all_rounds = game_status['number_of_all_rounds']
    return render(request, 'end_round.html', {'round_winner': round_winner, 'number_of_played_rounds': number_of_played_rounds, 'number_of_all_rounds': number_of_all_rounds, 'game_id': game_id})

#        game_winner = game_status['game_winner']
#        number_of_played_rounds = game_status['number_of_played_rounds']
#        if game_status['player1_wins']: 
#            player1_wins = game_status['player1_wins']
#        if game_status['player2_wins']: 
#            player2_wins = game_status['player2_wins']
#        return render(request, 'end')

def end_game(request, game_id):
    game_status = game_manager.get_game_status(game_id)
    if game_status['Game ended']:
        if game_status['winner']:
            winner = game_status['winner']
        else:
            tie = 'It\'s a tie!'
        number_of_played_rounds = game_status['number_of_played_rounds']
        if game_status['player1_wins']: 
            player1_wins = game_status['player1_wins']
        if game_status['player2_wins']: 
            player2_wins = game_status['player2_wins']
        return render(request, 'end.html', {'winner': game_winner, 'tie': tie, 'number_of_played_rounds': number_of_played_rounds, 'player1_wins': player1_wins, 'player1': player1 ,'player2_wins': player2_wins, 'player2': player2})
    else:
        return HttpResponseRedirect(reverse('view_round', args=(game_id,)))
#    player = game_manager.player_on_turn(game_id)
#    if player == False:
#        return redirect('home')
#    # delete_game(game_id)
#    # delete_game_after_x_seconds(game_id, 120)
    return render(request, 'end.html', {'player' : player})

#def admin_page(request):
#    return render(request, 'admin.html', {'all_games_data': get_all_games_data()})

def handler404(request):
    return render(request, '404.html', status=404)
