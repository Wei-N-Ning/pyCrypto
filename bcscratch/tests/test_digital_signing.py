import textwrap
import unittest

import nacl.encoding
import nacl.exceptions
import nacl.signing


class TestDigitalSigning(unittest.TestCase):
    def setUp(self):
        self.bob_private_key = nacl.signing.SigningKey.generate()
        self.bob_pub_key = self.bob_private_key.verify_key

    def test_sign_document(self):
        # in order to publish the key to the receivers of the document
        # I need to serialize it to a readable format
        bob_pub_key_hex = self.bob_pub_key.encode(encoder=nacl.encoding.HexEncoder)
        document = textwrap.dedent('''
        Hi,
        I am writing to let you know ....
        
        There is a cow
        ''')
        signed = self.bob_private_key.sign(document.encode())

        # the signed doc is not encrypted. I can still see the plain text
        self.assertTrue(signed)

        # generate the verify-key
        verify_key = nacl.signing.VerifyKey(bob_pub_key_hex, encoder=nacl.encoding.HexEncoder)

        # verify
        o = verify_key.verify(signed).decode()
        self.assertEqual(document, o)

        # tampering the signed document, then verify() will throw an error
        self.assertRaises(nacl.exceptions.BadSignatureError, verify_key.verify, signed + b' ')
