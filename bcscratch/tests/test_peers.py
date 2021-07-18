import json
import textwrap
import unittest

import marshmallow

from bcscratch.peers import *


class TestPeerSerialization(unittest.TestCase):
    def setUp(self) -> None:
        self.p1 = {'ip': '0.0.0.0', 'port': 5000, 'last_seen': 111}
        self.p2s = textwrap.dedent('''
            {"ip": "192.168.0.12", "port": 8080, "last_seen": 12312}
        ''')

    def test_serialization(self):
        s = Peer().dumps(self.p1)
        d = json.loads(s)
        self.assertEqual(self.p1, d)

    def test_deserialization(self):
        d = Peer().loads(self.p2s)
        self.assertEqual({"ip": "192.168.0.12", "port": 8080, "last_seen": 12312}, d)

    def test_serialize_expect_null(self):
        s = Peer().dumps({'_unknown_field_': '___'})
        self.assertEqual(s, '{}')

    def test_deserialize_broken_json_expect_raise(self):
        self.assertRaises(
            json.decoder.JSONDecodeError,
            Peer().loads,
            '{"ip": "192.168.0.12", "port'
        )

    def test_deserialize_missing_required_field_expect_raise(self):
        self.assertRaises(
            marshmallow.exceptions.ValidationError,
            Peer().loads,
            '{"ip": "192.168.0.12"}'
        )

    def test_deserialize_has_irrelevant_field_expect_raise(self):
        self.assertRaises(
            marshmallow.exceptions.ValidationError,
            Peer().loads,
            '{"ip": "192.168.0.12", "port": 8080, "last_seen": 12312, "some": 1}'
        )
