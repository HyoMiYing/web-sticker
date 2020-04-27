from sticker import Sticker, Igra
from threading import Timer

sticker_game_engine = Sticker()
dictionary_of_custom_names = {}
dictionary_of_descriptions = {}

class WebStickerGameManager(object):

    def __init__(self):
        self.dictionary_of_games = {}

    def find_new_id_in_dictionary_of_games(self):
        if self.dictionary_of_games == {}:
            return 0
        else:
            return max(self.dictionary_of_games.keys()) + 1

    def instantiate_new_WebStickerGame(self, cleaned_form_data):
        new_instance = WebStickerGame(cleaned_form_data)
        id_of_new_instance = self.find_new_id_in_dictionary_of_games()
        self.dictionary_of_games[id_of_new_instance] = new_instance
        return id_of_new_instance

class WebStickerGame(object):

    def __init__(self, cleaned_form_data):
        self.player1 = cleaned_form_data['player1']
        self.player2 = cleaned_form_data['player2']
        self.number_of_rounds = cleaned_form_data['number_of_rounds']
        self.description = cleaned_form_data['game_description']

def create_custom_names_for_the_game(form_data, game_id):
    dictionary_of_custom_names[game_id] = {'player1': form_data['player1'], 'player2': form_data['player2']}

def create_description_for_game(description, game_id):
    dictionary_of_descriptions[game_id] = description

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
    current_player = game_instance.player
    current_player_name = dictionary_of_custom_names[game_id][current_player]
    return current_player_name

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
        information_dictionary = {'game_id': game, 'game_position': game_position(game), 'player_on_turn': player_on_turn(game), 'description': dictionary_of_descriptions[game]}
        all_games_data.append(information_dictionary)
    return all_games_data
