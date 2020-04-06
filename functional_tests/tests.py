from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from django.test import LiveServerTestCase
import time

class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def validate_current_player(self, current_player):
        player_in_HTML = self.browser.find_element_by_id('id_player').text
        self.assertEqual(current_player, player_in_HTML)

    def remove_cards_from_row(self, row_number, number_of_cards):
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
            return 'There is not enough cards in this row!'

        submit_button = self.browser.find_element_by_id('id_submit_button').click()

        cards_in_observed_row = self.browser.find_elements_by_css_selector(f'label[for^="id_row{row_number-1}card"]')
        if len(cards_in_observed_row) == number_of_chosen_cards - number_of_cards:
            return 'Removal successful'
        else:
            raise AssertionError

    def test_user_can_play_a_game_with_himself(self):
        # Kinda silly I know

        # Rok visits the home page
        self.browser.get(self.live_server_url)
        self.assertIn('Sticker', self.browser.title)

        # He notices there is a 'show instructions' link on the page
        show_instructions_link = self.browser.find_element_by_link_text('Show instructions')
        show_instructions_link.click()

        # Now he can read the game rules
        game_rules = self.browser.find_element_by_id('id_game_rules').text
        self.assertIn('The player who picks up the last card, loses.', game_rules)

        # Because Rok hasn't got any friends nearby at the moment, he decides to play the game with himself (Like that old granpa from the short Pixar movie)
        # He selects the card in the top row (It is the only card there)
        self.validate_current_player('player1')
        self.remove_cards_from_row(1, 1)

        # After the page refreshes, Rok can see it says it's 'player2's turn now, and the 0_0 card is gone
        self.validate_current_player('player2')

        # Now Rok assumes he is player2 and removes all cards from the last row
        self.remove_cards_from_row(4, 2)

        # Then, again there is player1's turn and he removes 2 cards from 2nd row
        self.validate_current_player('player1')
        self.remove_cards_from_row(2, 2)

        # 'player2' then removes all cards in the 3rd row
        self.validate_current_player('player2')
        self.remove_cards_from_row(3, 5)

        # Now there's only player1's turn and he removes all the cards left in the 4th row
        self.validate_current_player('player1')
        self.remove_cards_from_row(4, 5)

        # Now, player2 has only one option - to remove the last card from the board, which was in the 2nd row
        self.validate_current_player('player2')
        self.remove_cards_from_row(2, 1)

        # The game is over. Winner is player1 (because player2 picked up the last card)
        self.assertIn('player1, you won!', self.browser.find_element_by_tag_name('body').text)
        # And there is also a link to another game
        self.browser.find_element_by_link_text('Play New Game')

   def test_multiple_players_can_play_on_different_urls(self):
        # next day: write out this test... help yourself with the example in TDD book.

# Write test for error messages (no card selected)
# Cards from different rows (error message or just invalid input)
