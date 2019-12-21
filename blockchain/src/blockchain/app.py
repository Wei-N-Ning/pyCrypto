import argparse
import sys
import uuid

import flask

from .lib import BlockChain

app = flask.Flask('simple blockchain')
node_identifier = str(uuid.uuid4()).replace('-', '')
blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    TO do three things:

    - calculate the proof of work
    - reward the miner by adding a transaction granting us 1 coin
    - forge the new Block by adding it to the chain
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(sender='0', recipient=node_identifier, amount=1)

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    resp = {
        'message': 'New Block has been forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return flask.jsonify(resp), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = flask.request.get_json()
    if not (values
            and all([values.get(k)
                     for k in ('sender', 'recipient', 'amount')])):
        return 'Missing values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'],
                                       values['amount'])
    resp = {'message': f'Transaction will be added to Block {index}'}
    return flask.jsonify(resp), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return flask.jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = flask.request.get_json()
    if not values.get('nodes'):
        return 'expect a list of nodes', 400
    for node in values['nodes']:
        blockchain.register_node(node)
    resp = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return flask.jsonify(resp), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    if blockchain.resolve_conflicts():
        resp = {
            'message': 'chain has been replaced',
            'new_chain': blockchain.chain
        }
    else:
        resp = {'message': 'chain is the source of truth'}
    return flask.jsonify(resp), 200


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=5000)
    arg = parser.parse_args(sys.argv[1:])
    app.run(host=arg.address, port=arg.port)
