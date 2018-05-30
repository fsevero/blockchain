# Initialize our blockchain list
blockchain = []


def get_last_blockchain_value():
    """ Returns the last value on the current blockchain. """
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """ Append a new value and the last blockchain at the blockchain.

    Arguments:
        :transaction_amount: The amount to be added
        :last_transaction: The old blockchain transaction (default [1])
    """
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    """ Asks the user to the amount of the transaction
    and returns as a float """
    return float(input('Your transaction amount, please: '))


tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(transaction_amount=tx_amount,
          last_transaction=get_last_blockchain_value())

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

print(blockchain)
