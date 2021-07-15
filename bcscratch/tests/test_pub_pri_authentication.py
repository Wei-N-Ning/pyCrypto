import unittest

from nacl.public import PrivateKey, Box


class TestPublicPrivateKeyAuthentication(unittest.TestCase):
    def setUp(self):
        self.alice_private_key = PrivateKey.generate()
        self.alice_pub_key = self.alice_private_key.public_key
        self.bob_private_key = PrivateKey.generate()
        self.bob_pub_key = self.bob_private_key.public_key

    def test_bob_send_alice_msg(self):
        # bob creates a box with his private key
        bob_box = Box(self.bob_private_key, self.alice_pub_key)
        encrypted = bob_box.encrypt('there is a cow'.encode())

        # alice to decrypt the msg
        alice_box = Box(self.alice_private_key, self.bob_pub_key)
        plain = alice_box.decrypt(encrypted).decode()

        self.assertEqual(plain, 'there is a cow')
