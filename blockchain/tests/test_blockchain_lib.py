from blockchain.lib import BlockChain

import unittest


class TestBlockChain(unittest.TestCase):
    def setUp(self):
        self.bc = BlockChain()

    def test_create_initial_blockchain(self):
        self.assertTrue(self.bc)

    def test_new_transaction(self):
        r1 = self.bc.new_transaction('wei@c', 'ning@d', 1231)
        r2 = self.bc.new_transaction('wei@c', 'ning@d', 11)
        self.assertEqual(r1, 2)
        self.assertEqual(r2, 2)
