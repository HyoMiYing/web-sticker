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

    def print_functionality(self, functionality):
        return_of_functionality = exec(functionality)
        dir_of_functionality = dir(return_of_functionality)

    def validate_current_player(self, current_player):
        player_in_HTML = self.browser.find_element_by_id('id_player').text
        self.assertEqual(current_player, player_in_HTML)

    def validate_current_player_in_foreign_browser(self, current_player, browser):
        player_in_HTML = browser.find_element_by_id('id_player').text
        self.assertEqual(current_player, player_in_HTML)

    def remove_cards_from_row_in_foreign_browser(self, number_of_cards, row_number, browser):
        # Select all cards from row
        chosen_cards = browser.find_elements_by_css_selector(f'label[for^="id_row{row_number-1}card"]')
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

        submit_button = browser.find_element_by_id('id_submit_button').click()

        cards_in_observed_row = browser.find_elements_by_css_selector(f'label[for^="id_row{row_number-1}card"]')
        if len(cards_in_observed_row) == number_of_chosen_cards - number_of_cards:
            return 'Removal successful'
        else:
            raise AssertionError

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

    def start_new_game(self, player1, player2, number_of_rounds=3):
        player1_field = self.browser.find_element_by_id('id_player1')
        player2_field = self.browser.find_element_by_id('id_player2')
        number_of_rounds_field = self.browser.find_element_by_id('id_number_of_rounds')
        submit_button = self.browser.find_element_by_id('id_submit_button')

        player1_field.send_keys(player1)
        player2_field.send_keys(player2)
        for option in number_of_rounds_field.find_elements_by_tag_name('option'):
            if option.text == f'{number_of_rounds} rounds':
                option.click()
                break

        time.sleep(0.5)
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

    def test_end_game_data_is_correct(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Sticker', self.browser.title)

        self.start_new_game('Rok', 'Kor', 3)

        # He notices there is a 'show instructions' link on the page
        show_instructions_link = self.browser.find_element_by_link_text('Show instructions')
        show_instructions_link.click()

        # Now he can read the game rules
        game_rules = self.browser.find_element_by_id('id_game_rules').text
        self.assertIn('The player who picks up the last card, loses', game_rules)

	# He plays a round
        self.play_a_round('Rok', 'Kor')

        # The round 1 of 3 is over. Winner is Rok (because Kor picked up the last card)
        self.assert_correct_player_has_won_this_round('Rok', 1)
        self.assert_round_x_of_y_is_finished(1, 3)

	# He pesses continue link to proceed to another round
        continue_link = self.browser.find_element_by_link_text('Continue') 
        continue_link.click()
        time.sleep(0.5)

	# He plays another round
        self.play_a_round('Rok', 'Kor')

        # The round 2 of 3 is over. Winner is Rok (because Rok picked up the last card)
        self.assert_correct_player_has_won_this_round('Rok', 2)
        self.assert_round_x_of_y_is_finished(2, 3)

        continue_link = self.browser.find_element_by_link_text('Continue') 
        continue_link.click()
        time.sleep(0.5)

	# He plays the last round
        self.play_a_round('Rok', 'Kor')

        # The round 3 of 3 is over. Now the winner of the whole game is Rok.
	# That is because Rok had won 3 games and Rok had won 0 games.
        self.assertIn('Rok, you won the game!', self.browser.find_element_by_tag_name('body').text)
        self.assertIn('Number of rounds Rok won: 3', self.browser.find_element_by_tag_name('body').text)
        self.assertIn('Number of rounds Kor won: 0', self.browser.find_element_by_tag_name('body').text)

        # And there is also a link to another game
        self.browser.find_element_by_link_text('Play New Game')



    def test_user_can_play_a_game_with_himself(self):
        # Kinda silly I know

        # Rok visits the home page
        self.browser.get(self.live_server_url)
        self.assertIn('Sticker', self.browser.title)

        # He is invited to start a new game by providing player1 name, player2 name, a game description and number of rounds.
	# Since he is playing with himself, he enters both player1 and player2 as 'Rok'.
	# Game description is 'Just playing with myself'. He also choses to play the least number of
	# rounds (3)
        self.start_new_game('Rok', 'Rok', 3)

        # He notices there is a 'show instructions' link on the page
        show_instructions_link = self.browser.find_element_by_link_text('Show instructions')
        show_instructions_link.click()

        # Now he can read the game rules
        game_rules = self.browser.find_element_by_id('id_game_rules').text
        self.assertIn('The player who picks up the last card, loses', game_rules)

	# He plays a round
        self.play_a_round('Rok', 'Rok')

        # The round 1 of 3 is over. Winner is Rok (because Rok picked up the last card)
        self.assert_correct_player_has_won_this_round('Rok', 1)
        self.assert_round_x_of_y_is_finished(1, 3)

	# He pesses continue link to proceed to another round
        continue_link = self.browser.find_element_by_link_text('Continue') 
        continue_link.click()
        time.sleep(0.5)

	# He plays another round
        self.play_a_round('Rok', 'Rok')

        # The round 2 of 3 is over. Winner is Rok (because Rok picked up the last card)
        self.assert_correct_player_has_won_this_round('Rok', 2)
        self.assert_round_x_of_y_is_finished(2, 3)

        continue_link = self.browser.find_element_by_link_text('Continue') 
        continue_link.click()
        time.sleep(0.5)

	# He plays the last round
        self.play_a_round('Rok', 'Rok')

        # The round 3 of 3 is over. Now the winner of the whole game is Rok.
	# That is because Rok had won 3 games and Rok had won 0 games.
        self.assertIn('Rok, you won the game!', self.browser.find_element_by_tag_name('body').text)

        # And there is also a link to another game
        self.browser.find_element_by_link_text('Play New Game')

    def test_multiple_players_can_play_on_different_urls(self):
    # This test proves that application can run multiple games on different URLs
        # Rok visits the homepage
        self.browser.get(self.live_server_url)

        # He starts new game
        self.start_new_game('Rok', 'Rok', 3)
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
        self.start_new_game('Dino', 'Dean', 11)
        # There is no sign of Rok's moves!
        cards_in_second_row = self.browser.find_elements_by_css_selector('label[for^="id_row1card"]')
        self.assertEquals(len(cards_in_second_row), 3, f'There are {cards_in_second_row} cards in second row. There should be only 3')

        # Dino is playing his own game
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
        self.start_new_game('The Bamboozler', 'The Bamboozler', 5)

        # He sees a new game form, full of cards. The Bamboozler
        # decides to submit an empty form.
        submit_button = self.browser.find_element_by_id('id_submit_button')
        submit_button.click()

        # The page submits but returns with an error
        self.assertIn('You must select at least one card', self.browser.find_element_by_class_name('errorlist').text)

	# Surprised, that his bamboozlin' plan didn't work out, he decides to turn off the computer
	# untill he gets a new bamboozle idea
    @unittest.skip
    def test_games_can_be_played_between_two_players_online_without_them_having_to_refresh_the_page(self):
        # Sacre Bleu finds cool new online game
        self.browser.get(self.live_server_url)

        # He sees it is a 2 player game. He decides he will play the game with his friend, Jacques.
        self.start_new_game('Sacre Bleu', 'Jacques', 5)

        # Now Sacre Bleu makes a move
        self.validate_current_player('Sacre Bleu')
        self.remove_cards_from_row(1, 1)

        # Now it is Jacques's turn
        self.validate_current_player('Jacques')

        # But Jacques isn't online yet. He doesn't even know that the game exists.
	# Sacre Bleu decides that he will send the website's link to Jacques by SMS.
	# He sends him an sms: "Éh! Quoi de neuf? Moi, Sacre Bleu have make a great discovery!
	# Un grand online game, Sticker! It is for un intellectuels like tu et moi! Let's play!
	# www.the-game-website.com"

	# Now Sacre Bleu decides to wait. He leaves the Sticker tab to be open and goes to read Wikipedia
        self.browser.execute_script("window.open('');")
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.get('https://en.wikipedia.org')

	# After some time, Jacques reads Sacre Bleu's SMS and goes to the Sticker homepage.
        self.browserJacques = webdriver.Firefox()
        self.browserJacques.get(self.live_server_url)

	# There he sees a list of all running games. He finds the description saying 'Bonjour Jacques, join this game!'
        the_games_description_id = self.browserJacques.find_element_by_xpath('//td[text()="Bonjour Jacques, join this game!"]').get_attribute('id')

        # Then he presses the Visit Game link accompanying the description
        id_of_sacres_and_jacques_game = list(the_games_description_id)[-1]
        the_correct_visit_game_link = self.browserJacques.find_element_by_id('id_link_to_game'+id_of_sacres_and_jacques_game)
        the_correct_visit_game_link.click()

	# Now Jacques finds himself in the game, and it is his turn!
        self.validate_current_player_in_foreign_browser('Jacques', self.browserJacques)

	# He reads the instructions and decides to remove all cards from the thrid row
        self.remove_cards_from_row_in_foreign_browser(5, 3, self.browserJacques)

	# Now It is Sacre Bleu's turn
        self.validate_current_player_in_foreign_browser('Sacre Bleu', self.browserJacques)

	# Meanwhile Sacre Bleu is reading Wikipedia.
	# Suddenly he notices that Sticker's browser tab title is messaging him "It is your turn" and "Sticker"
        self.assertIn('Wiki', self.browser.title)
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.assertIn('Sticker', self.browser.title)
        time.sleep(1)
	# He sees it really is his turn
        self.validate_current_player('Sacre Bleu')
	# Then Sacre Bleu says to himself: "Oh, seigneur! This webpage is très bien fait! I can go rest
	# now."
	# Jacques is confused, because Sacre Bleu doesn't make a move. Tired of waiting he also goes
	# to rest.
        self.browserJacques.quit()

    @unittest.skip
    def test_home_html_is_able_to_update_itself(self):
        # The Moderator goes to the homepage of the application(he's just there)
        the_moderators_window = webdriver.Firefox()
        the_moderators_window.get(self.live_server_url)
        self.assertIn('Sticker Home', the_moderators_window.title)
	# He doesn't see any 'Rok' playin' the Sticker game...
        self.assertNotIn('Rok', the_moderators_window.page_source)

	# Rok wakes up from his power nap
	# It is time for another good ol' game with himself
        self.browser.get(self.live_server_url)
        self.start_new_game('Rok', 'Rok')
        time.sleep(0.5)

        # The Moderator is still on the watch. He is eating doughnuts and sippin' coffee when suddenly
	# Rok's name appears on screen. It appears he is playin' a game...
        self.assertIn('Rok', the_moderators_window.page_source)
	# The Moderator says to himself: "Another successful day of watching over the internet"
	# Then, he goes offline.
        the_moderators_window.quit()
