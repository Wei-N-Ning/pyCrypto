import unittest
import requests


class TestGetPrice(unittest.TestCase):
    def test_get_price(self):
        url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
        response = requests.get(url)
        self.assertTrue(response)
        self.assertTrue(response.text)
        print(response.text)
