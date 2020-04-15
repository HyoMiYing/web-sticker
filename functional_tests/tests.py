from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import unittest
import os

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

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

    def start_new_game(self, player1, player2, game_description):
        player1_field = self.browser.find_element_by_id('id_player1')
        player2_field = self.browser.find_element_by_id('id_player2')
        game_description_field = self.browser.find_element_by_id('id_game_description')
        submit_button = self.browser.find_element_by_id('id_submit_button')

        player1_field.send_keys(player1)
        player2_field.send_keys(player2)
        game_description_field.send_keys(game_description)
        submit_button.click()

    def test_user_can_play_a_game_with_himself(self):
        # Kinda silly I know

        # Rok visits the home page
        self.browser.get(self.live_server_url)
        self.assertIn('Sticker', self.browser.title)

        # He is invited to start a new game by providing player1 name, player2 name and a game description.
	# Since he is playing with himself, he enters both player1 and player2 as 'Rok'. Game description in 'Just playing with myself'
        self.start_new_game('Rok', 'Rok', 'Just playing with myself')

        # He notices there is a 'show instructions' link on the page
        show_instructions_link = self.browser.find_element_by_link_text('Show instructions')
        show_instructions_link.click()

        # Now he can read the game rules
        game_rules = self.browser.find_element_by_id('id_game_rules').text
        self.assertIn('The player who picks up the last card, loses.', game_rules)

        # He selects the card in the top row (It is the only card there)
        self.validate_current_player('Rok')
        self.remove_cards_from_row(1, 1)

        # After the page refreshes, Rok can see it says it's 'Rok's turn now, and the 0_0 card is gone
        self.validate_current_player('Rok')

        # Now Rok removes all cards from the last row
        self.remove_cards_from_row(2, 4)

        # Then, again there is Rok's turn and he removes 2 cards from 2nd row
        self.validate_current_player('Rok')
        self.remove_cards_from_row(2, 2)

        # Rok then removes all cards in the 3rd row
        self.validate_current_player('Rok')
        self.remove_cards_from_row(5, 3)

        # Now there's Rok's turn and he removes all the cards left in the 4th row
        self.validate_current_player('Rok')
        self.remove_cards_from_row(5, 4)

        # Now, Rok has only one option - to remove the last card from the board, which was in the 2nd row
        self.validate_current_player('Rok')
        self.remove_cards_from_row(1, 2)

        # The game is over. Winner is Rok (because Rok picked up the last card)
        self.assertIn('Rok, you won!', self.browser.find_element_by_tag_name('body').text)
        # And there is also a link to another game
        self.browser.find_element_by_link_text('Play New Game')

    def test_multiple_players_can_play_on_different_urls(self):
    # This test proves that application can run multiple games on different URLs
        # Rok visits the homepage
        self.browser.get(self.live_server_url)

        # He starts new game
        self.start_new_game('Rok', 'Rok', 'Še en dan, še ena igra')
        self.validate_current_player('Rok')
        self.remove_cards_from_row(3, 2)
        cards_in_second_row = self.browser.find_elements_by_css_selector('label[for^="id_row1card"]')

        # He notices that his game has a unique URL
        rok_game_url = self.browser.current_url
        self.assertRegex(rok_game_url, '/game/.+')

        # Now a user Dino comes along to the site
        
        ## We use a new browser session to make sure
        ## no cookies are giving us information about Rok
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Dino visits the home page.
        self.browser.get(self.live_server_url)
	# He starts his own game.
        self.start_new_game('Dino', 'Dean', 'Đe si brate! Daj, ajmo!')
        # There is no sign of Rok's moves!
        cards_in_second_row = self.browser.find_elements_by_css_selector('label[for^="id_row1card"]')
        self.assertEquals(len(cards_in_second_row), 3, f'There are {cards_in_second_row} cards in second row. There should be only 3')

        # Dino plays his own game
        self.validate_current_player('Dino')
        self.remove_cards_from_row(1, 1)

        # Dino's game gets his own unique URL
        self.validate_current_player('Dean')
        dino_game_url = self.browser.current_url
        self.assertRegex(dino_game_url, '/game/.+')
        self.assertNotEqual(dino_game_url, rok_game_url)

        # And once again, there is no sign of Rok's move
        cards_in_second_row = self.browser.find_elements_by_css_selector('label[for^="id_row1card"]')
        self.assertEquals(len(cards_in_second_row), 3, f'There are {cards_in_second_row} cards in second row. There should be only 3')

        # Satisfied, they both go party.

    def test_submitting_empty_form_returns_error_message(self):
        # The Bamboozler goes to visit the Sticker website
        self.browser.get(self.live_server_url)

	# He creates new game
        self.start_new_game('The Bamboozler', 'The Bamboozler', 'Here i go bamboozlin\' again!')

        # He sees a new game form, full of cards. The Bamboozler
        # decides to submit an empty form.
        submit_button = self.browser.find_element_by_id('id_submit_button')
        submit_button.click()

        # The page submits but returns with an error
        self.assertIn('You must select at least one card', self.browser.find_element_by_class_name('errorlist').text)
