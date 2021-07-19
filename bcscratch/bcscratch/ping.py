from marshmallow import Schema, fields


class Ping(Schema):
    block_height = fields.Int(required=True)
    peer_count = fields.Int(required=True)
    is_miner = fields.Boolean(required=True)
