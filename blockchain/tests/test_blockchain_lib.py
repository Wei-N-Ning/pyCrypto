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

    def test_register_node(self):
        self.bc.register_node('http://wei.com:342')
        self.assertEqual(len(self.bc.nodes), 1)

    def test_new_block(self):
        last_proof = self.bc.last_block['proof']
        proof = self.bc.proof_of_work(last_proof)
        self.bc.new_block(proof)
        self.assertEqual(len(self.bc.chain), 2)

    def test_validate_chain(self):
        self.assertFalse(self.bc.valid_chain(self.bc.chain))

        last_proof = self.bc.last_block['proof']
        proof = self.bc.proof_of_work(last_proof)
        b = self.bc.new_block(proof)

        self.assertTrue(self.bc.valid_chain(self.bc.chain))

        proof2 = self.bc.proof_of_work(proof)
        b2 = self.bc.new_block(proof2)

        self.assertTrue(self.bc.valid_chain(self.bc.chain))
        self.assertFalse(self.bc.valid_chain([b, b, b, b]))
