import hashlib
import json
import random
from datetime import datetime


class Blockchain:
    def __init__(self):
        self.chain = list()
        self.pending_transactions = list()
        self._create_genesis_block()

    def _create_genesis_block(self):
        self.chain.append(self.new_block())

    @staticmethod
    def gen_nonce(size=64):
        return format(random.getrandbits(size), 'x')

    def new_block(self, prev_hash=None) -> dict:
        block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().isoformat(),
            'transactions': self.pending_transactions,
            'prev_hash': prev_hash,
            'nonce': None,  # non-sense
            # P/48
            # think of nonce as a one-off random number, which will be
            # used as an important source of randomness for our blocks
        }
        block['hash'] = self.hash(block)
        self.pending_transactions = list()
        return block

    @staticmethod
    def hash(block) -> str:
        return hashlib.sha256(
            json.dumps(block, sort_keys=True, indent=None).encode()
        ).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def length(self):
        return len(self.chain)

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

    def proof_of_work(self):
        while True:
            new_block = self.new_block()
            if self.valid_block(new_block):
                self.chain.append(new_block)
                return new_block

    @staticmethod
    def valid_block(block):
        """
        The number of zeros define the difficulty of mining

        The addition of a single zero makes an exponential difference
        to the time required to find a solution.

        Args:
            block:

        Returns:

        """
        return block['hash'].startswith('0000')
