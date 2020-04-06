from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class FunctionalTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_smoke(self):
        # Rok visits the home page
        self.browser.get(self.live_server_url)
        self.assertIn('Sticker', self.browser.title)
