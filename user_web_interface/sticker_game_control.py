from sticker import Sticker, Igra

sticker_game_engine = Sticker()

def print_all_games():
    dictonary_of_games = sticker_game_engine.igre
    return dictonary_of_games

def new_game():
    game_id = sticker_game_engine.new_game([1, 3, 5, 7])
    return game_id
    
def game_position(game_id):
    dictionary_of_all_game_instances = sticker_game_engine.igre
    current_game_instance = dictionary_of_all_game_instances[game_id]
    return current_game_instance.position

def player_on_turn(game_id):
    game_instance = sticker_game_engine.igre[game_id]
    return game_instance.player

def remove_cards(row_number, number_of_cards, game_id):
    game_instance = sticker_game_engine.igre[game_id]

    move_function = game_instance.move(int(row_number)+1, number_of_cards)

    return move_function

def delete_game(game_id):
    if sticker_game_engine.remove_id(game_id):
        return 'Game instance deleted'
    else:
        return 'ERROR, not deleted'