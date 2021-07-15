import hashlib
import unittest

import PIL


def hash_string(s: str) -> str:
    """
    bitcoin uses double sha256
    Ethererum uses keccak256

    Args:
        s:

    Returns:

    """
    return hashlib.sha512(s.encode('utf-8')).hexdigest()


def hash_img(img: PIL.Image) -> str:
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


class TestHashThings(unittest.TestCase):
    def test_hash_word(self):
        o = hash_string('hello world')
        self.assertTrue(o)
        print(o)

    def test_hash_image(self):
        img = PIL.Image.new('RGB', (8, 8), "black")  # Create a new black image
        pixels = img.load()  # Create the pixel map
        for i in range(img.size[0]):  # For every pixel:
            for j in range(img.size[1]):
                pixels[i, j] = (i, j, 100)  # Set the colour accordingly
        o = hash_img(img)
        self.assertTrue(o)
        print(o)
