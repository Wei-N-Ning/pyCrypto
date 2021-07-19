from marshmallow import Schema, fields, post_load
from marshmallow_oneofschema import OneOfSchema

from bcscratch.block import Block
from bcscratch.peers import Peer
from bcscratch.ping import Ping
from bcscratch.transactions import Transaction


class PeersMessage(Schema):
    payload = fields.Nested(Peer, many=True)

    @post_load
    def add_name(self, data, **kwargs):
        """
        Notes on `post_load`: Register a method to invoke after deserializing an object
        Args:
            data:
            **kwargs:

        Returns:

        """
        data['name'] = 'peers'
        return data


class BlockMessage(Schema):
    payload = fields.Nested(Block)

    @post_load
    def add_name(self, data, **kwargs):
        data['name'] = 'block'
        return data


class TransactionMessage(Schema):
    payload = fields.Nested(Transaction)

    @post_load
    def add_name(self, data, **kwargs):
        data['name'] = 'transaction'
        return data


class PingMessage(Schema):
    payload = fields.Nested(Ping)

    @post_load
    def add_name(self, data, **kwargs):
        data['name'] = 'ping'
        return data


class MessageDisambiguation(OneOfSchema):
    type_field = 'name'
    type_schemas = {
        'ping': PingMessage,
        'peers': PeersMessage,
        'block': BlockMessage,
        'transaction': TransactionMessage,
    }

    def get_obj_type(self, obj):
        if isinstance(obj, dict):
            return obj.get('name')
        return ''


class MetaSchema(Schema):
    address = fields.Nested(Peer)
    client = fields.Str()


class BaseSchema(Schema):
    meta = fields.Nested(MetaSchema)
    message = fields.Nested(MessageDisambiguation)


def create_peers_message(external_ip: str, external_port: int, peers):
    return ''


def create_block_message(external_ip: str, external_port: int, block):
    return ''


def create_transaction_message(external_ip: str, external_port: int, tx):
    return ''


def create_ping_message(external_ip: str, external_port: int, length, n_peers, switch):
    return ''
