import asyncio
import unittest

from bcscratch import blockchain


class TestBlockchain(unittest.TestCase):
    def setUp(self) -> None:
        """
        make the mining difficulty super low to save time

        """
        self.chain = blockchain.Blockchain()
        self.chain.target = '0' + 'f' * 63

    def test_create_and_initialize_chain(self):
        self.assertTrue(self.chain.last_block())
        print(self.chain.last_block())
        self.assertEqual(1, self.chain.length())

    def test_create_new_block_not_validated(self):
        b1 = self.chain.new_block()
        self.assertTrue(b1.hash)
        self.assertTrue(b1.prev_hash)
        self.assertEqual(1, self.chain.length())

    def test_ensure_target_recalculation(self):
        old_target = self.chain.target
        for _ in range(12):
            asyncio.run(self.chain.mine_new_block())
        new_target = self.chain.target
        self.assertNotEqual(old_target, new_target)
        self.assertLess(new_target, old_target)
