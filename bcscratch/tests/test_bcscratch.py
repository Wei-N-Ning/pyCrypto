import unittest

from bcscratch import __version__


class TestSome(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, '0.1.0')
