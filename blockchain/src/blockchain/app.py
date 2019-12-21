import json
import uuid

import flask

from .lib import BlockChain

app = flask.Flask('simple blockchain')
node_identifier = uuid.uuid4()
blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    return 'mining a new block'


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return 'adding a new transaction'


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return json.jsonify(response), 200


def main():
    app.run(host='0.0.0.0', port=5000)
