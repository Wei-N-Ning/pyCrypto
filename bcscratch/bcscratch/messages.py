import dataclasses


class BaseSchema:
    def loads(self, payload: str):
        pass


def create_peers_message(external_ip: str, external_port: int, peers):
    return ''


def create_block_message(external_ip: str, external_port: int, block):
    return ''


def create_transaction_message(external_ip: str, external_port: int, tx):
    return ''


def create_ping_message(external_ip: str, external_port: int, length, n_peers, switch):
    return ''
