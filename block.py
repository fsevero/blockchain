from time import time

class Block:
    def __init__(self, index, previous_hash, transactions, proof, time_=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time() if time_ is None else time_
        self.transactions = transactions
        self.proof = proof
