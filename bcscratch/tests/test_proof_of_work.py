import hashlib
import random
import time
import unittest


def generate(size: int) -> [int]:
    return random.choices(list(range(100)), k=size)


def do_hash(payload: [int]) -> str:
    return hashlib.sha256(bytes(payload)).hexdigest()


def prove(h: str) -> bool:
    """
    Super low mining difficulty to save time
    Args:
        h:

    Returns:

    """
    return int('0x' + h[:7], 16) < 100000


def trial() -> [int]:
    s = time.time()
    while True:
        payload = generate(12)
        if prove(do_hash(payload)):
            return payload, time.time() - s


class TestProofOfWork(unittest.TestCase):
    def test_average_time(self):
        _, time_taken = trial()
        self.assertGreater(time_taken, 0.0001)
