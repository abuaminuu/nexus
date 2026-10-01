"""
Docstring for testing client side part of the application
"""
from django.test import TestCase
import os
import unittest
import pathlib
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# find uniform resource identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()



# Standard outline of testing class
class WebpageTests(unittest.TestCase):

    def setUp(self):
        # setup browser web driver
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
    
    def test_title(self):
        """Make sure title is correct"""
        self.driver.get(file_uri("counter.html"))

        # wait 5s for page to load
        WebDriverWait(self.driver, 5).until(EC.title_is("Counter"))

        # assert
        self.assertEqual(self.driver.title, "Counter")

if __name__ == "__main__":
    unittest.test()
