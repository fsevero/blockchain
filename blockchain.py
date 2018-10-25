from functools import reduce
import hashlib as hl
import json
from collections import OrderedDict


MINING_REWARD = 10.0

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Severo'
participants = {owner}


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hl.sha256(guess).hexdigest()
    return guess_hash[0:4] == '0000'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def hash_block(block):
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)

    amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received - amount_sent

def get_last_blockchain_value():
    """ Returns the last value on the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value and the last blockchain at the blockchain.

    Arguments:
        :sender: The sender of the coins
        :recipient: The recipient of the coins
        :amount: The amount of coins sent with the transaction (default = 1.0)
    """
    transaction = OrderedDict([
        ('sender', sender),
        ('recipient', recipient),
        ('amount', amount)
    ])

    if not verify_transaction(transaction):
        return False

    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)
    return True


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINING_REWARD)
    ])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }

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


def verify_chain():
    """ Validates if each elements contain the previous
    and their are equal """
    for index, block in enumerate(blockchain):
        if index == 0:
            continue

        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False

        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False

    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print('-' * 10)
    print('Please, choose:')
    print('1: Add a new blockchain transaction')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
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

    elif user_choice == '3':
        print_blockchain_elements()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')

    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = genesis_block = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Max', 'recipient': 'Severo', 'amount': 100.00}]
            }

    elif user_choice == 'q':
        waiting_for_input = False

    else:
        print('Invalid input!')

    if not verify_chain():
        print_blockchain_elements()
        print('Invalid chain!!!')
        break

    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('Bye!')
