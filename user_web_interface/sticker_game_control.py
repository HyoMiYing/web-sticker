from sticker import Sticker, Igra
from threading import Timer
import re


class WebStickerGameManager(object):

    def __init__(self):
        self.dictionary_of_games = {}

    def get_admin_data(self):
        game_touples = []
        for element in self.dictionary_of_games:
            game_instance = self.dictionary_of_games[element]
            touple = (f'Player 1: {game_instance.player1}', f'Player 2: {game_instance.player2}', f'Number of rounds: {game_instance.number_of_rounds}')
            game_touples.append(touple)
        return game_touples

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

    def instantiate_new_mashine_WebStickerGame(self, data_from_form):
        form_data = {}
        form_data['player2'] = 'The Mashine'
        form_data['player1'] = data_from_form['your_name']
        form_data['number_of_rounds'] = data_from_form['number_of_rounds']
        new_instance = WebStickerGame(form_data)
        id_of_new_instance = self.find_new_id_in_dictionary_of_games()
        self.dictionary_of_games[id_of_new_instance] = new_instance
        return id_of_new_instance        

    def get_winner(self, game_id):
        correct_game = self.dictionary_of_games[game_id]
        winner = correct_game.last_winner
        return winner

    def get_player_name(self, player_number, game_id):
        correct_game = self.dictionary_of_games[game_id]
        if player_number == 1:
            player_name = correct_game.player1
        elif player_number == 2:
            player_name = correct_game.player2
        else:
            raise Exception('Player number should be either 1 or 2.')
        return player_name

    def get_game_status(self, game_id):
        correct_game = self.dictionary_of_games[game_id]
        number_of_played_rounds = correct_game.current_round - 1
        number_of_all_rounds = correct_game.number_of_rounds
        if number_of_played_rounds == number_of_all_rounds:
            if correct_game.player1_wins == correct_game.player2_wins:
                game_status_dictionary = {'tie': True}
            elif correct_game.player1_wins > correct_game.player2_wins:
                game_status_dictionary = {'winner': correct_game.player1}
            elif correct_game.player2_wins > correct_game.player1_wins:
                game_status_dictionary = {'winner': correct_game.player2}
            else:
                raise Exception('Wrong player win value.')            
            game_status_dictionary.update({'Game over': True, 'number_of_played_rounds': number_of_played_rounds, 'player1_wins': str(correct_game.player1_wins), 'player2_wins': str(correct_game.player2_wins), 'player1': correct_game.player1, 'player2': correct_game.player2}) 
            return game_status_dictionary
        return {'number_of_played_rounds': number_of_played_rounds, 'number_of_all_rounds': number_of_all_rounds}

    def get_round_information(self, game_id):
        correct_game = self.dictionary_of_games[game_id]
        round_information = correct_game.get_round_information()
        return round_information

    def remove_cards(self, post_data, game_id):
        correct_game = self.dictionary_of_games[game_id]
        removal_message = correct_game.remove_cards(post_data)
        return removal_message

    def make_the_mashine_move(self, game_id):
        correct_game = self.dictionary_of_games[game_id]
        removal_message = correct_game.make_the_mashine_move()
        return removal_message

class WebStickerGame(object):

    def __init__(self, cleaned_form_data):
        self.player1 = cleaned_form_data['player1']
        self.player2 = cleaned_form_data['player2']
        self.number_of_rounds = int(cleaned_form_data['number_of_rounds'])
        self.current_round = 1
        self.lukas_sticker = Sticker()
        [self.lukas_sticker.new_game() for round in range(self.number_of_rounds)]
        self.last_winner = None
        self.player1_wins = 0
        self.player2_wins = 0

    def get_round_information(self):
        # Go to Igra class and read player and position values
        try:
            current_game = self.lukas_sticker.igre[self.current_round-1]
        except KeyError:
            return 'Game over'
        current_games_position = current_game.position
        current_player = current_game.player
        if current_player == 'player1' and self.current_round % 2 == 1:
            current_player_name = self.player1
            current_player_number = 1
        elif current_player == 'player1' and self.current_round % 2 == 0:
            current_player_name = self.player2
            current_player_number = 2
        elif current_player == 'player2' and self.current_round % 2 == 1:
            current_player_name = self.player2
            current_player_number = 2
        elif current_player == 'player2' and self.current_round % 2 == 0:
            current_player_name = self.player1
            current_player_number = 1
        else:
            raise Exception('Current player should be either player1 or player2')
        return {'player': current_player_name, 'position': current_games_position, 'player_number': current_player_number}

    def clean_POST_data(self, data):
        csrf_token = data.pop(0)
        row_number_in_first_card = int(list(data[0])[3]) + 1
        for card in data:
            if (int(list(card)[3]) + 1) == row_number_in_first_card:
                row_number = row_number_in_first_card
            else:
                row_number = False
        number_of_cards = len(data)
        return {'row_number': row_number, 'number_of_cards': number_of_cards}
        
    def remove_cards(self, post_data):
        cleaned_POST_data = self.clean_POST_data(post_data)
        current_game = self.lukas_sticker.igre[self.current_round-1]
        move_message = current_game.move(cleaned_POST_data['row_number'], cleaned_POST_data['number_of_cards'])
        if re.search('Game over', move_message):
            player_number = list(move_message)[-1]
            self.set_last_winner(str(player_number))
            self.current_round += 1
        return move_message

    def make_the_mashine_move(self):
        current_game = self.lukas_sticker.igre[self.current_round-1]
        move_message = current_game.move_maschine('biginner')
        if re.search('Game over', move_message):
            player_number = list(move_message)[-1]
            self.set_last_winner(str(player_number))
            self.current_round += 1
        return move_message


    def set_last_winner(self, player_number):
        if player_number == '1' and self.current_round % 2 == 1:
            self.last_winner = self.player1
            self.player1_wins += 1
        elif player_number == '1' and self.current_round % 2 == 0:
            self.last_winner = self.player2
            self.player2_wins += 1
        elif player_number == '2' and self.current_round % 2 == 1:
            self.last_winner = self.player2
            self.player2_wins += 1
        elif player_number == '2' and self.current_round % 2 == 0:
            self.last_winner = self.player1
            self.player1_wins += 1
        else:
            raise Exception('Player number should be 1 or 2.')
