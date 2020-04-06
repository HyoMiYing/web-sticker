from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_can_play_a_game_by_himself(self):
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
        the_0_0_card = self.browser.find_element_by_css_selector('label[for="id_row0card0"]')
        the_0_0_card.click()
        self.fail('Finish the test!')
