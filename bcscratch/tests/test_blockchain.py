import asyncio
import unittest

from bcscratch import blockchain


class TestBlockchain(unittest.TestCase):
    def test_create_and_initialize_chain(self):
        chain = blockchain.Blockchain()
        self.assertTrue(chain.last_block())
        print(chain.last_block())
        self.assertEqual(1, chain.length())

    def test_create_new_block_not_validated(self):
        chain = blockchain.Blockchain()
        b1 = chain.new_block()
        self.assertTrue(b1.hash)
        self.assertTrue(b1.prev_hash)
        self.assertEqual(1, chain.length())

    def test_create_new_block_validated_chained(self):
        chain = blockchain.Blockchain()
        b1 = chain.proof_of_work()
        self.assertEqual(2, chain.length())
        self.assertTrue(b1.hash.startswith('0000'))

    def test_ensure_target_recalculation(self):
        chain = blockchain.Blockchain()
        old_target = chain.target
        for _ in range(12):
            asyncio.run(chain.mine_new_block())
        new_target = chain.target
        self.assertNotEqual(old_target, new_target)
        self.assertLess(new_target, old_target)
