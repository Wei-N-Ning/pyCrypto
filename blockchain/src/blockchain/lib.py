import hashlib
import json
import time
from urllib.parse import urlparse

import requests


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
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
        return guess_hash.startswith('0000')

    def register_node(self, address):
        """
        Params:
            address: address of the node
                     e.g. http://192.168.0.5:5000
        """
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        Params:
            chain: a blockchain.chain

        Returns:
            bool
        """
        last_block = chain[0]
        if len(chain) < 2:
            return False
        for block, block_next in zip(chain, chain[1:]):
            if block_next['previous_hash'] != self.hash(block):
                return False
            if not self.valid_proof(block['proof'], block_next['proof']):
                return False
        return True

    def resolve_conflicts(self):
        """
        The consensus algorithm.

        It resolves conflicts by replacing our chain with the longest one in the network.

        Returns:
            bool
        """
        new_chain = None
        max_length = len(self.chain)
        for node in self.nodes:
            resp = requests.get(f'http://{node}/chain')
            length = resp.json()['length']
            chain = resp.json()['chain']
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False
