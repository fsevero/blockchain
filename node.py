from flask import Flask, jsonify
from flask_cors import CORS

from blockchain import Blockchain
from wallet import Wallet

app = Flask(__name__)
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

@app.route('/', methods=['GET'])
def get_ui():
    return 'This works!'

@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()

    global blockchain
    blockchain = Blockchain(wallet.public_key)
    
    if wallet.save_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance(),
        }
        status = 201
    else:
        response = {
            'message': 'Saving the keys failed.'
        }
        status = 500

    return jsonify(response), status

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)

        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance(),
        }
        status = 201
    else:
        response = {
            'message': 'Loading the keys failed.'
        }
        status = 500

    return jsonify(response), status

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance is not None:
        response = {
            'message': 'Fetched balance successfully.',
            'funds': balance,
        }
        status = 200
    else:
        response = {
            'message': 'Loading balance failed.',
            'is_wallet_set_up': wallet.public_key != None,
        }
        status = 500
    return jsonify(response), status

@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    
    if block:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block added sucessfully.',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        status = 201
    else:
        response = {
            'message': 'Adding a block failed.',
            'is_wallet_set_up': wallet.public_key != None,
        }
        status = 500
    return jsonify(response), status

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_blocks in dict_chain:
        dict_blocks['transactions'] = [tx.__dict__.copy() for tx in dict_blocks['transactions']]
    return jsonify(dict_chain), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')