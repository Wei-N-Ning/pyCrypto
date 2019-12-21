import hashlib
import json
import time


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block and adds it to the chain
        
        Params:
            proof: the proof given by the proof of work algorithm
            previous hash: hash of previous block

        Returns:
            new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # reset the current list of transcations
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Adds a new transaction to the list of transactions

        Creates a new transaction to go into the next mined Block
        
        Params:
            sender: address of the sender
            recipient: address of the recipient
            amount: amount
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        Params:
            block: Block

        Returns:
            str
        """
        s = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(s).hexdigest()

    @property
    def last_block(self):
        """Returns the last block in the chain
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        - Find a number p' such as hash(pp') contains leading 4 zeros,
        - p is the previous proof, and p' is the new proof

        Params:
            last_proof: int

        Returns:
            new proof
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the given proof: hash(last_proof, proof) contain 4 leading zeroes
        
        To adjust the difficulty of the algorithm, modify the number of leading zeroes
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith('00000')
