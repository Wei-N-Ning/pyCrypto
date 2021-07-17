
from bcscratch.block import Block

import time
import unittest


class TestBlockInterface(unittest.TestCase):
    def test_creation(self):
        b = Block(1, [], '0001', '', '000f', time.time())
        self.assertTrue(b.hash)
