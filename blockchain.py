# Initialize our blockchain list
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Severo'


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


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
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    open_transactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }

    blockchain.append(block)


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

    return True


waiting_for_input = True

while waiting_for_input:
    print('-' * 10)
    print('Please, choose:')
    print('1: Add a new blockchain transaction')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: QUIT')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_data = get_transaction_value()
        tx_recipient, tx_amount = tx_data
        add_transaction(tx_recipient, amount=tx_amount)

    elif user_choice == '2':
        mine_block()

    elif user_choice == '3':
        print_blockchain_elements()

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
else:
    print('Bye!')
