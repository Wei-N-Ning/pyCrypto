import hashlib
import json
from datetime import datetime


class Blockchain:
    def __init__(self):
        self.chain = list()
        self.pending_transactions = list()
        self._create_genesis_block()

    def _create_genesis_block(self):
        self.new_block()

    def new_block(self, prev_hash=None) -> dict:
        block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().isoformat(),
            'transactions': self.pending_transactions,
            'prev_hash': prev_hash,
        }
        block['hash'] = self.hash(block)
        self.pending_transactions = list()
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block) -> str:
        return hashlib.sha256(
            json.dumps(block, sort_keys=True, indent=None).encode()
        ).hexdigest()

    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
