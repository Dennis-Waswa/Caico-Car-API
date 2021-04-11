# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:55:33 2021

@author: Dennis Waswa
"""


import uuid
# Represents an insurance claim
class Claim:
    def __init__(self, customer_id, date, incident_description, claim_amount):
        self.ID = str(uuid.uuid1())
        self.customer_id = customer_id
        self.date = date
        self.incident_description = incident_description
        self.claim_amount = claim_amount
        self.approved_amount = 0
        self.status = "UNKNOWN"

    def setStatus(self, status, approved_amount):
        self.status = status
        self.approved_amount = approved_amount

    # convert object to JSON
    def serialize(self):
        return {
            'id': self.ID,
            'date': self.date,
            'incident_description': self.incident_description,
            'customer_id': self.customer_id,
            'claim_amount': self.claim_amount,
            'status': self.status,
            'approved_amount': self.approved_amount
        }
