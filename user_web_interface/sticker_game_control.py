from sticker import Sticker, Igra
from threading import Timer

sticker_game_engine = Sticker()

#def create_custom_names_for_the_game(form_data, game_id):
#   get the dictionary of all {'custom_games':'custom_names'}
#
#
#

def print_all_games():
    dictonary_of_games = sticker_game_engine.igre
    return dictonary_of_games

def new_game():
    game_id = sticker_game_engine.new_game([1, 3, 5, 7])
    return game_id
    
def game_position(game_id):
    dictionary_of_all_game_instances = sticker_game_engine.igre
    try:
        current_game_instance = dictionary_of_all_game_instances[game_id]
    except KeyError:
        return False
    return current_game_instance.position

def player_on_turn(game_id):
    try:
        game_instance = sticker_game_engine.igre[game_id]
    except KeyError:
        return False
    return game_instance.player

def clean_POST_data(data):
    csrf_token = data.pop(0)
    row_number_in_first_card = int(list(data[0])[3]) + 1
    for card in data:
        if (int(list(card)[3]) + 1) == row_number_in_first_card:
            row_number = row_number_in_first_card
        else:
            row_number = False
    number_of_cards = len(data)
    return {'row_number': row_number, 'number_of_cards': number_of_cards}

def remove_cards(data, game_id):
    cleaned_POST_data = clean_POST_data(data)
    game_instance = sticker_game_engine.igre[game_id]
    move_function = game_instance.move(cleaned_POST_data['row_number'], cleaned_POST_data['number_of_cards'])
    return move_function

def delete_game(game_id):
    if sticker_game_engine.remove_id(game_id):
        return 'Game instance deleted'
    else:
        return 'ERROR, not deleted'

def delete_game_after_x_seconds(game_id, time_in_seconds):
    new_thread = Timer(time_in_seconds, delete_game(game_id))
    new_thread.start()

def get_game_information(game_id):
    position = game_position(game_id)
    if not position:
        return False
    player = player_on_turn(game_id)
    return {'position': position, 'player': player}

def delete_game(game_id):
    sticker_game_engine.remove_id(game_id)

def get_all_games_data():
    all_games_data = []
    for game in sticker_game_engine.igre:
        information_dictionary = {'game_id': game, 'game_position': game_position(game), 'player_on_turn': player_on_turn(game)}
        all_games_data.append(information_dictionary)
    return all_games_data
