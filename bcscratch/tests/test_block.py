import hashlib
import json

from bcscratch.block import Blk, Block

import time
import unittest

from bcscratch.transactions import Transaction


class TestBlockInterface(unittest.TestCase):
    def setUp(self):
        self.trans = {'timestamp': 1, 'sender': 'doom', 'receiver': 'dune', 'amount': 1, 'signature': 'e1m1'}
        self.trans_dump = Transaction().dumps(self.trans)
        self.schema = Block()

    def test_creation(self):
        b = Blk(1, [], '0001', '', '000f', time.time())
        self.assertTrue(b.hash)

    def test_schema_validation(self):
        b = {'mined_by': 'doom', 'transactions': [self.trans], 'height': 112, 'target': 'dune', 'prev_hash': 'xas',
             'nonce': '23', 'timestamp': 11}
        good_hash = hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()
        b['hash'] = good_hash
        s = self.schema.dumps(b)
        b2 = self.schema.loads(s)
        self.assertEqual(b, b2)
