from functools import reduce
import json
import pickle

from block import Block
from hash_util import hash_block
from transaction import Transaction
from verification import Verification


MINING_REWARD = 10.0

genesis_block = Block(0, '', [], 100, 0)
blockchain = [genesis_block]
open_transactions = []
owner = 'Severo'


# def save_data():
#     with open('blockchain', mode='wb') as f:
#         save_data = {
#             'chain': blockchain,
#             'ot': open_transactions
#         }
#         f.write(pickle.dumps(save_data))


# def load_data():
#     with open('blockchain', mode='rb') as f:
#         file_content = pickle.loads(f.read())
#         global blockchain
#         global open_transactions

#         blockchain = file_content['chain']
#         open_transactions = file_content['ot']


def save_data():
    with open('blockchain.txt', mode='w') as f:
        tx_converted_blockchain = [Block(block.index, block.previous_hash, [tx.to_ordered_dict() for tx in block.transactions], block.proof, block.timestamp) for block in blockchain]
        savable_chain = [block.__dict__ for block in tx_converted_blockchain]
        f.write(json.dumps(savable_chain))
        f.write('\n')
        savable_transaction = [tx.__dict__ for tx in open_transactions]
        f.write(json.dumps(savable_transaction))


def load_data():
    with open('blockchain.txt', mode='r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions

        blockchain = json.loads(file_content[0])
        updated_blockchain = []
        for block in blockchain:
            transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
            updated_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain

        open_transactions = json.loads(file_content[1])
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions

try:
    load_data()
except (IOError, IndexError):
    save_data()  # Create a new file only with the genesis block


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns the last value on the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value and the last blockchain at the blockchain.

    Arguments:
        :sender: The sender of the coins
        :recipient: The recipient of the coins
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = Transaction(sender, recipient, amount)

    verifier = Verification()
    if not verifier.verify_transaction(transaction, get_balance):
        return False

    open_transactions.append(transaction)
    save_data()
    return True


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Asks the user to the amount of the transaction
    and returns as a float """
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount, please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """ Asks the user for the menu choices """
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Prints each block of the blockchain """
    for block in blockchain:
        print(block)

waiting_for_input = True

while waiting_for_input:
    print('-' * 10)
    print('Please, choose:')
    print('1: Add a new blockchain transaction')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Check transaction validity')
    print('q: QUIT')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        tx_recipient, tx_amount = tx_data
        if add_transaction(tx_recipient, amount=tx_amount):
            print('Added transaction')
        else:
            print('Transaction failed')

    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_blockchain_elements()

    elif user_choice == '4':
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print('All transactions are valid')
        else:
            print('There are invalid transactions')

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('Invalid input!')

    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print('Invalid chain!!!')
        break

    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('Bye!')
