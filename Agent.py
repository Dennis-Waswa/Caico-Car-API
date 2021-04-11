# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:55:33 2021

@author: Dennis Waswa
"""


import uuid
# Represents the insurance agent
class Agent:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.customers = []

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name,
            'address': self.address
        }

    def addCustomer(self, customer):
        self.customers.append(customer)

    def deleteCustomer(self, customer):
        for c in self.customers:
            if customer.ID == c.ID:
                self.customers.remove(customer)
                return True
        return False
