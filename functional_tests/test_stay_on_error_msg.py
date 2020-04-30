from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import unittest
import os

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')

    def tearDown(self):
        pass

    def validate_current_player(self, current_player):
        player_in_HTML = self.browser.find_element_by_id('id_player').text
        self.assertEqual(current_player, player_in_HTML)

    def remove_cards_from_row(self, number_of_cards, row_number):
        # Select all cards from row
        chosen_cards = self.browser.find_elements_by_css_selector(f'label[for^="id_row{row_number-1}card"]')
        number_of_chosen_cards = len(chosen_cards)
        # If it's okay, select them. If there are too much cards, put them away
        # and the select the right amount of them.
        if len(chosen_cards) == number_of_cards:
            for card in chosen_cards:
                card.click()
        elif len(chosen_cards) > number_of_cards:
            sorted_cards = chosen_cards[0:number_of_cards]
            for card in sorted_cards:
                card.click()
        else:
            return self.fail('There is not enough cards in this row!')

        submit_button = self.browser.find_element_by_id('id_submit_button').click()

        cards_in_observed_row = self.browser.find_elements_by_css_selector(f'label[for^="id_row{row_number-1}card"]')
        if len(cards_in_observed_row) == number_of_chosen_cards - number_of_cards:
            return 'Removal successful'
        else:
            raise AssertionError

    def start_new_game(self, player1, player2, game_description, number_of_rounds=3):
        player1_field = self.browser.find_element_by_id('id_player1')
        player2_field = self.browser.find_element_by_id('id_player2')
        game_description_field = self.browser.find_element_by_id('id_game_description')
        number_of_rounds_field = self.browser.find_element_by_id('id_number_of_rounds')
        submit_button = self.browser.find_element_by_id('id_submit_button')

        player1_field.send_keys(player1)
        player2_field.send_keys(player2)
        game_description_field.send_keys(game_description)
        for option in number_of_rounds_field.find_elements_by_tag_name('option'):
            if option.text == f'{number_of_rounds} rounds':
                option.click()
                break

        time.sleep(1.5)
        submit_button.click()

    def assert_round_x_of_y_is_finished(self, x, y):
        number_of_finished_rounds = f'{x}'
        number_of_finished_rounds_in_HTML = self.browser.find_element_by_id('id_finished_rounds').text
        number_of_all_rounds = f'{y}'
        number_of_all_rounds_in_HTML = self.browser.find_element_by_id('id_all_rounds').text
        self.assertIn(number_of_finished_rounds, number_of_finished_rounds_in_HTML)
        self.assertIn(number_of_all_rounds, number_of_all_rounds_in_HTML)

    def assert_correct_player_has_won_this_round(self, winning_player, round_number):
        end_of_round_declaration = self.browser.find_element_by_id('id_end_of_round_information').text
        self.assertIn(f'{winning_player} won round {round_number}', end_of_round_declaration)

    def play_a_round(self, player1, player2):
	#player1 always wins
        self.validate_current_player(player1)
        self.remove_cards_from_row(1, 1)
        self.validate_current_player(player2)
        self.remove_cards_from_row(3, 2)
        self.validate_current_player(player1)
        self.remove_cards_from_row(5, 3)
        self.validate_current_player(player2)
        self.remove_cards_from_row(7, 4)

    def test_user_can_play_a_game_with_himself(self):
        # Kinda silly I know

        # Rok visits the home page
        self.browser.get('http://localhost:8000')
        self.assertIn('Sticker', self.browser.title)

        # He is invited to start a new game by providing player1 name, player2 name, a game description and number of rounds.
	# Since he is playing with himself, he enters both player1 and player2 as 'Rok'.
	# Game description is 'Just playing with myself'. He also choses to play the least number of
	# rounds (3)
        self.start_new_game('Rok', 'Rok', 'Just playing with myself', 3)

        # He notices there is a 'show instructions' link on the page
        show_instructions_link = self.browser.find_element_by_link_text('Show instructions')
        show_instructions_link.click()

        # Now he can read the game rules
        game_rules = self.browser.find_element_by_id('id_game_rules').text
        self.assertIn('The player who picks up the last card, loses.', game_rules)

	# He plays a round
        self.play_a_round('Rok', 'Rok')

        # The round 1 of 3 is over. Winner is Rok (because Rok picked up the last card)
        self.assert_correct_player_has_won_this_round('Rok', 1)
        self.assert_round_x_of_y_is_finished(1, 3)

	# He pesses continue link to proceed to another round
        continue_link = self.browser.find_element_by_link_text('Continue') 
        continue_link.click()
        time.sleep(1.5)

	# He plays another round
        self.play_a_round('Rok', 'Rok')

        # The round 2 of 3 is over. Winner is Rok (because Rok picked up the last card)
        self.assert_correct_player_has_won_this_round('Rok', 2)
        self.assert_round_x_of_y_is_finished(2, 3)

        continue_link = self.browser.find_element_by_link_text('Continue') 
        continue_link.click()
        time.sleep(1.5)

	# He plays the last round
        self.play_a_round('Rok', 'Rok')

        # The round 3 of 3 is over. Now the winner of the whole game is Rok.
	# That is because Rok had won 3 games and Rok had won 0 games.
        self.assertIn('Rok, you won the game!', self.browser.find_element_by_tag_name('body').text)

        # And there is also a link to another game
        self.browser.find_element_by_link_text('Play New Game')
