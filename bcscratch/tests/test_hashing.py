import hashlib
import unittest

from PIL import Image


def hash_string(s: str) -> str:
    """
    bitcoin uses double sha256
    Ethererum uses keccak256

    Args:
        s:

    Returns:

    """
    return hashlib.sha512(s.encode('utf-8')).hexdigest()


def hash_img(img: Image) -> str:
    """
    reference:
    https://stackoverflow.com/questions/30658193/python3-how-to-make-a-bytes-object-from-a-list-of-integers

    if the image comes from storage (.jpg, .png etc.), then
    just read it in as bytes `rb`

    Args:
        img:

    Returns:

    """
    return hashlib.sha512(b''.join(bytes(b3) for b3 in img.getdata())).hexdigest()


def hash_secret(msg: str, scr: str) -> str:
    return hash_string(msg + scr)


def verify_message(msg: str, h: str, scr: str) -> bool:
    return hash_string(msg + scr) == h


class TestHashThings(unittest.TestCase):
    def test_hash_word(self):
        o = hash_string('hello world')
        self.assertTrue(o)
        print(o)

    def test_hash_image(self):
        img = Image.new('RGB', (8, 8), "black")  # Create a new black image
        pixels = img.load()  # Create the pixel map
        for i in range(img.size[0]):  # For every pixel:
            for j in range(img.size[1]):
                pixels[i, j] = (i, j, 100)  # Set the colour accordingly
        o = hash_img(img)
        self.assertTrue(o)
        print(o)

    def test_hash_message_with_secret(self):
        msg = 'there is a cow'
        scr = 'e1m1_iddqd'
        o = hash_secret(msg, scr)
        self.assertTrue(verify_message(msg, o, scr))
        self.assertFalse(verify_message('there is a c0w', o, scr))
