"""
The blockchain data structure and manipulators
"""
import asyncio
import math
import random
import time
from typing import *

import structlog

from bcscratch.block import Block
from bcscratch.block import Transaction

logger = structlog.get_logger()

ValidatorT = Callable[[Block], bool]


class Blockchain:
    def __init__(self):
        # to set to mining difficulty
        self.target: str = '00' + 'f' * 62

        self.chain: List[Block] = list()
        self.pending_transactions: List[Transaction] = list()

        # initialization
        self._create_genesis_block()

    def _create_genesis_block(self):
        self.chain.append(self.new_block())

    @staticmethod
    def gen_nonce(size=64):
        return format(random.getrandbits(size), 'x')

    def new_block(self) -> Block:
        return Block(
            len(self.chain),
            self.pending_transactions,
            self.last_block().hash if self.length() else None,
            self.gen_nonce(),
            self.target,
            time.time()
        )

    def new_valid_block(self, f: ValidatorT) -> Optional[Block]:
        b = self.new_block()
        if not f(b):
            return None
        self.pending_transactions = list()
        return b

    def last_block(self):
        return self.chain[-1]

    def length(self):
        return len(self.chain)

    def new_transaction(self, sender, recipient, amount) -> Transaction:
        tx = Transaction(
            sender,
            recipient,
            amount,
        )
        self.pending_transactions.append(tx)
        return tx

    def add_block(self, block):
        self.chain.append(block)

    def proof_of_work(self) -> Block:
        """
        The number of zeros define the difficulty of mining

        The addition of a single zero makes an exponential difference
        to the time required to find a solution.

        Returns:
            a newly created, validated block
        """
        while True:
            new_block = self.new_valid_block(lambda b: b.hash.startswith('0000'))
            if new_block is not None:
                self.chain.append(new_block)
                return new_block

    def recalculate_target(self, block_index: int) -> str:
        """
        Returns the number (some kind of threshold) we need to get below to mine a block.

        Args:
            block_index: (height) the index number given to a block at its birth

        Returns:
            the new target if recalculated or the current target

            (recall that target sets the mining difficulty)
        """
        if block_index > 0 and block_index % 10 == 0:
            expected_timespan = 10 * 10
            actual_timespan = self.last_block().timestamp - self.chain[-10].timestamp
            ratio = actual_timespan / expected_timespan
            ratio = min(4.0, max(0.25, ratio))
            new_target = int(self.target, 16) * ratio
            self.target = format(math.floor(new_target), 'x').zfill(64)
            logger.info(f'Calculated new mining target: {self.target}')
        return self.target

    async def get_blocks_after_timestamp(self, timestamp):
        for index, block in enumerate(self.chain):
            if timestamp < block.timestamp:
                return self.chain[index:]

    async def mine_new_block(self):
        """
        same as proof_of_work() method except:
        - is async
        - the validation logic changes: here it checks whether the block's hash is less
                then the target (string comparison, BAD!)
                the target gets increasingly smaller as more blocks are added
        """
        self.recalculate_target(self.last_block().index)
        while True:
            new_block = self.new_valid_block(lambda b: b.hash < self.target)
            if new_block is not None:
                await asyncio.sleep(0)
                self.add_block(new_block)
                logger.info(f'Found a new block: {new_block}')
                return new_block
