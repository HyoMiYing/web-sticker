from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from user_web_interface.sticker_game_control import new_game, game_position, player_on_turn, remove_cards, delete_game, print_all_games
from user_web_interface.forms import GameForm

def home(request):

    # Create new game instance
    current_game_id = new_game()

    # Access the data of the new game instance
    game_instance_position = game_position(current_game_id)
    game_instance_player_on_turn = player_on_turn(current_game_id)

    # Generate form
    form = GameForm(game_instance_position)

    return render(request, 'home.html', {'form':form, 'current_player':game_instance_player_on_turn, 'game_id':current_game_id})

def make_a_move(request, game_id):

    # Form validation
    game_instance_position = game_position(game_id)
    game_instance_player_on_turn = player_on_turn(game_id)
    form = GameForm(game_instance_position, request.POST)

    if form.is_valid():
        print('Form is valid')

        queryset_keys = list(request.POST.keys())
        csrf_token = queryset_keys.pop(0)
        number_of_cards = len(queryset_keys)
        row_number = list(queryset_keys[0])[3]

        message_of_removal = remove_cards(row_number, number_of_cards, game_id)
        last_character_of_the_message_of_removal = list(message_of_removal)[-1]

        if last_character_of_the_message_of_removal == '1' or last_character_of_the_message_of_removal == '2':
            return HttpResponseRedirect(reverse('end_game', args=(game_id,)))
        else:
            return HttpResponseRedirect(reverse('view_game', args=(game_id,)))
    else:
        print('Form is not valid')
        print(f'Form.errors is={form.errors}')
        return render(request, 'home.html', {'form':form, 'current_player':game_instance_player_on_turn, 'game_id':game_id})


    # Refine the POST data to get the row and number of cards removed from the said row
    




def view_game(request, game_id):

    # Access the data of the new game instance
    game_instance_position = game_position(game_id)
    game_instance_player_on_turn = player_on_turn(game_id)

    # Generate form
    form = GameForm(game_instance_position)

    return render(request, 'home.html', {'form':form, 'current_player':game_instance_player_on_turn, 'game_id':game_id})

def end_game(request, game_id):
    player = player_on_turn(game_id)
    return HttpResponse(f'the winner is {player}.')