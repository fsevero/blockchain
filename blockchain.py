from functools import reduce
import json
import pickle

from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verification
from wallet import Wallet


MINING_REWARD = 10.0


class Blockchain:

    def __init__(self, hosting_node_id):
        self.__chain = [Block(0, '', [], 100, 0)]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id

        self.load_data()

        self.__peer_nodes = set()

    @property
    def chain(self):
        return self.__chain[:]

    @property
    def open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        # with open('blockchain', mode='rb') as f:
        #     file_content = pickle.loads(f.read())
        #     global blockchain
        #     global open_transactions

        #     blockchain = file_content['chain']
        #     open_transactions = file_content['ot']
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0])
                updated_blockchain = []
                for block in blockchain:
                    transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain

                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                self.__peer_nodes = set(json.loads(file_content[2]))
        except (IOError, IndexError):
            pass
        finally:
            pass

    def save_data(self):
        # with open('blockchain', mode='wb') as f:
        #     save_data = {
        #         'chain': blockchain,
        #         'ot': open_transactions
        #     }
        #     f.write(pickle.dumps(save_data))
        with open('blockchain.txt', mode='w') as f:
            tx_converted_blockchain = [Block(block.index, block.previous_hash, [tx.to_ordered_dict() for tx in block.transactions], block.proof, block.timestamp) for block in self.__chain]
            savable_chain = [block.__dict__ for block in tx_converted_blockchain]
            f.write(json.dumps(savable_chain))
            f.write('\n')
            savable_transaction = [tx.__dict__ for tx in self.__open_transactions]
            f.write(json.dumps(savable_transaction))
            f.write('\n')
            f.write(json.dumps(list(self.__peer_nodes)))

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        if not self.hosting_node:
            return None

        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)

        amount_sent = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_recipient, 0)

        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value on the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value and the last blockchain at the blockchain.

        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :signature: The wallet signature for the transaction
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        if not self.hosting_node:
            return False

        transaction = Transaction(sender, recipient, signature, amount)

        if not Verification.verify_transaction(transaction, self.get_balance):
            return False

        self.__open_transactions.append(transaction)
        self.save_data()
        return True

    def mine_block(self):
        if not self.hosting_node:
            return None

        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        copied_transactions = self.__open_transactions[:]

        for transaction in copied_transactions:
            if not Wallet.verify_transaction(transaction):
                return None

        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self, node):
        """adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """removes a new node from the peer node set.

        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()