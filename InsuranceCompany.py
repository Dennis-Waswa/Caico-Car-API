# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:58:18 2021

@author: Dennis Waswa
"""

from Customer import *
from Agent import *
from Claim import *
from Payment import *

class InsuranceCompany:
    def __init__(self, name):
        self.name = name # Name of the Insurance company
        self.customers = [] # list of customers
        self.agents = []  # list of dealers
        self.claims = []
        self.payments = []


    # Customer Methods

    def getCustomers(self):
        return list(self.customers)

    def addCustomer(self, name, address):
        c = Customer(name, address)
        self.customers.append(c)
        return c.ID

    def getCustomerById(self, id_):
        for c in self.customers:
            if(c.ID==id_):
                return c
        return None

    def deleteCustomer(self, customer_id):
        c = self.getCustomerById(customer_id)
        if (c==None):
            return False
        # remove the customer from the assigned agent list (if any)
        a = self.getAssignedAgent(customer_id)
        if (a!=None):
            a.deleteCustomer(c)

        # remove any claims that the customer has made (if any)
        for claim in self.claims:
            if claim.customer_id == c.ID:
                self.claims.remove(claim)

        # remove any payments that the customer has made (if any)
        for payment in self.payments:
            if payment.payer_id == c.ID:
                self.payments.remove(payment)

        self.customers.remove(c)
        return True

    def getAssignedAgent(self, customer_id):
        for agent in self.agents:
            for customer in agent.customers:
                if (customer_id==customer.ID):
                    return agent
        return None


    # Agent Methods
    def addAgent(self, name, address):
        a = Agent(name, address)
        self.agents.append(a)
        return a.ID

    def getAgentById(self, id_):
        for d in self.agents:
            if(d.ID==id_):
                return d
        return None

    def deleteAgent(self, agent_id):
        agent = self.getAgentById(agent_id)
        if (agent==None):
            return False

        # remove all payments associated with this agent
        for payment in self.payments:
            if (payment.payer_id==agent_id):
                self.payments.remove(payment)

        self.agents.remove(agent)
        return True

    def getAgents(self):
        return list(self.agents)


    #Insurance claim methods

    def getClaimByID(self, id_):
        for claim in self.claims:
            if (claim.ID == id_):
                return claim
        return None

    def addClaim(self, customer_id, date, incident_description, claim_amount):
        claim = Claim(customer_id, date, incident_description, claim_amount)
        self.claims.append(claim)
        return claim

    def addPayment(self, payment_type, date, payer_id, amount):
        p = Payment(payment_type, date, payer_id, amount)
        self.payments.append(p)
        return p

    def getPayments(self):
        return list(self.payments)
