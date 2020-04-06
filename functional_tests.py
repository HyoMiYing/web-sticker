import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import LiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Rok visits the home page
        self.browser.get(self.staging)