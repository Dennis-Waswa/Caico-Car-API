# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:55:33 2021

@author: Dennis Waswa
"""

import uuid
# Represents a payment (incoming or outgoing)
class Payment:
    def __init__(self, payment_type, date, payer_id, amount):
        self.ID = str(uuid.uuid1())
        self.date = date
        self.payment_type = payment_type
        self.payer_id = payer_id
        self.amount = amount

    # convert object to JSON
    def serialize(self):
        if (self.payment_type=="OUT"):
            return {'id': self.ID,
                    'date': self.date,
                    'agent_id': self.payer_id,
                    'amount_sent': self.amount,
            }

        return {
            'id': self.ID,
            'date': self.date,
            'customer_id': self.payer_id,
            'amount_received': self.amount,
        }
