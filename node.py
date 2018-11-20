from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:

    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'Severo'
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        """ Asks the user to the amount of the transaction
        and returns as a float """

        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount, please: '))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """ Asks the user for the menu choices """

        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """ Prints each block of the blockchain """
        for block in self.blockchain.chain:
            print(block)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print()
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))

            print('-' * 10)
            print('Please, choose:')
            print('1: Add a new blockchain transaction')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('q: QUIT')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                tx_recipient, tx_amount = tx_data
                if self.blockchain.add_transaction(tx_recipient, self.id, amount=tx_amount):
                    print('Added transaction')
                else:
                    print('Transaction failed')

            elif user_choice == '2':
                self.blockchain.mine_block()

            elif user_choice == '3':
                self.print_blockchain_elements()

            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')

            elif user_choice == 'q':
                waiting_for_input = False

            else:
                print('Invalid input!')

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid chain!!!')
                break

        else:
            print('Bye!')

node = Node()
node.listen_for_input()