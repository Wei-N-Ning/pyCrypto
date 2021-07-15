import unittest

from bcscratch import blockchain


class TestBlockchain(unittest.TestCase):
    def test_create_and_initialize_chain(self):
        chain = blockchain.Blockchain()
        self.assertTrue(chain.last_block())
        print(chain.last_block())

    def test_create_new_block(self):
        chain = blockchain.Blockchain()
        b1 = chain.new_block(prev_hash=chain.hash(chain.last_block()))
        self.assertTrue(b1['hash'])
        self.assertTrue(b1['prev_hash'])
