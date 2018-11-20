from printable import Printable
from collections import OrderedDict


class Transaction(Printable):

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self):
        return OrderedDict([
            ('sender', self.sender),
            ('recipient', self.recipient),
            ('amount', self.amount)
        ])