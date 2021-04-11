# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:56:36 2021

@author: Dennis Waswa
"""

from flask import Flask, request, jsonify
from InsuranceCompany import *
from Customer import *


app = Flask(__name__)

# Root object for the insurance company
company = InsuranceCompany("Be-Safe Insurance Company")

#-------------------------------------------------------------
# Customer HTTP Methods

#Add a new customer (parameters: name, address).
@app.route("/customer", methods=["POST"])
def addCustomer():
    # parameters are passed in the body of the request
    cid = company.addCustomer(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new customer with ID {cid}")

#Return the details of a customer of the given customer_id.
@app.route("/customer/<customer_id>", methods=["GET"])
def customerInfo(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        return jsonify(c.serialize())
    return jsonify(
            success = False,
            message = "Customer not found")

#Add a new car (parameters: model, numberplate).
@app.route("/customer/<customer_id>/car", methods=["POST"])
def addCar(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        car = Car(request.args.get('model'),
                  request.args.get('number_plate'),
                  request.args.get('motor_power'))
        c.addCar(car)

        return jsonify(
                success=True,
                message=f"Car added to customer with ID {customer_id}")

    return jsonify(
            success = False,
            message = "Customer not found")

@app.route("/customer/<customer_id>", methods=["DELETE"])
def deleteCustomer(customer_id):
    result = company.deleteCustomer(customer_id)
    if (result):
        message = f"Deleted customer with ID {customer_id}"
    else:
        message = "Customer not found"
    return jsonify(
            success = result,
            message = message)

@app.route("/customers", methods=["GET"])
def allCustomers():
    data = []

    for customer in company.getCustomers():
        customer_data = customer.serialize()
        customer_data['cars'] = [c.serialize() for c in customer.cars]
        data.append(customer_data)

    return jsonify(customers=data)


# Agent Methods

#Add a new insurance agent(parameters: name, address).
@app.route("/agent", methods=["POST"])
def addAgent():
    # parameters are passed in the body of the request
    aid = company.addAgent(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new agent with ID {aid}")

#Return the details of the agent with the given agent_id.
@app.route("/agent/<agent_id>", methods=["GET"])
def agentInfo(agent_id):
    a = company.getAgentById(agent_id)
    if(a!=None):
        return jsonify(a.serialize())

    return jsonify(
            success = False,
            message = "Agent not found")

#Assign a new customer with the provided customer_id to the agent with agent_id.
@app.route("/agent/<agent_id>/<customer_id>", methods=["POST"])
def assignCustomerToAgent(agent_id, customer_id):
    a = company.getAgentById(agent_id)
    c = company.getCustomerById(customer_id)
    if (a!=None and c!=None):
        assigned_agent = company.getAssignedAgent(customer_id)
        if (assigned_agent!=None):
            return jsonify(
                success=False,
                message=f"The customer with ID {customer_id} is already assigned to another agent with ID {assigned_agent.ID}.")

        a.addCustomer(c)
        return jsonify(
            success=True,
            message=f"Assigned agent with ID {a.ID} to customer with ID {c.ID}")

    elif (a==None):
        return jsonify(success=False, message=f"Agent not found")

    elif (c==None):
        return jsonify(success=False, message=f"Customer not found")

    return jsonify(success=False, message=f"Customer not found, and agent not found")

#Delete the agent with the given agent_id and move the assigned customers
@app.route("/agent/<agent_id>", methods=["DELETE"])
def deleteAgent(agent_id):
    a = company.getAgentById(agent_id)
    if (a==None):
        return jsonify(
                success = False,
                message = "Agent not found")

    if (len(company.agents)==1):
        if (len(a.customers)!=0):
            return jsonify(
                success=False,
                message="Can't delete the only one agent in the company with customers assigned!")

    # move all customers assigned to this agent to another agent
    for i, agent in enumerate(company.agents):
        if (agent.ID != agent_id):
            company.agents[i].customers.extend(a.customers)
            break

    # delete the agent from the company
    company.deleteAgent(agent_id)

    return jsonify(success=True, message="Deleted the agent and moved all of it's customers")

#Return a list of all agents.
@app.route("/agents", methods=["GET"])
def allAgents():
    data = []
    for agent in company.getAgents():
        agent_data = agent.serialize()
        agent_data["customers"] = [c.serialize() for c in agent.customers]
        data.append(agent_data)

    return jsonify(agents=data)


# Insurance Claim HTTP Methods

# Add a new insurance claim (parameters: date, incident_description, claim_amount).
@app.route("/claims/<customer_id>/file", methods=["POST"])
def addClaim(customer_id):
    date = request.args.get('date', default="", type=str)
    incident_description = request.args.get('incident_description', default="", type=str)
    claim_amount = request.args.get('claim_amount', default=-1, type=float)

    c = company.getCustomerById(customer_id)
    if (c==None):
        return jsonify(success=False, message="Customer not found")

    if (claim_amount<=0):
        return jsonify(success=False, message="Invalid claim amount")

    if (date==""):
        return jsonify(success=False, message="Invalid claim date")

    claim = company.addClaim(customer_id, date, incident_description, claim_amount)

    return jsonify(
            success=True,
            message=f"Claim added successfuly with ID {claim.ID}")

#Return details about the claim with the given claim_id.
@app.route("/claims/<claim_id>", methods=["GET"])
def claimInfo(claim_id):
    claim = company.getClaimByID(claim_id)
    if (claim==None):
        return jsonify(success=False, message="Claim not found")

    return jsonify(claim.serialize())

#Change the status of a claim to REJECTED, PARTLY COVERED or FULLY COVERED. Parameters: approved_amount.
@app.route("/claims/<claim_id>/status", methods=["PUT"])
def changeClaimStatus(claim_id):
    amount = request.args.get('approved_amount', default=-1, type=float)
    if (amount<0):
        return jsonify(success=False, message="Invalid amount")

    claim = company.getClaimByID(claim_id)
    if (claim==None):
        return jsonify(success=False, message="Claim not found")

    status = "REJECTED" if (amount==0) else \
             "PARTLY COVERED" if (amount<claim.claim_amount) else \
             "FULLY COVERED"

    claim.setStatus(status, amount)
    return jsonify(success=True, message=f"Changed the claim status to {status}")

#Return a list of all claims.
@app.route("/claims", methods=["GET"])
def allClaims():
    return jsonify(claims=[c.serialize() for c in company.claims])



#Payment HTTP Methods

#Add a new payment received from a customer. (parameters: date, customer_id, amount_received).
@app.route("/payment/in/", methods=["POST"])
def addIncomingPayment():
    date = request.args.get('date', default="", type=str)
    customer_id = request.args.get('customer_id', default="", type=str)
    amount_received = request.args.get('amount_received', default=-1, type=float)

    if (date==""):
        return jsonify(success=False, message="Invalid payment date")

    if (amount_received<0):
        return jsonify(success=False, message="Invalid amount")

    if (company.getCustomerById(customer_id)==None):
        return jsonify(success=False, message="Customer not found")

    company.addPayment("IN", date, customer_id, amount_received)
    return jsonify(success=True, message="Added an incoming payment successfuly.")

#Add a new payment transferred to an agent. (parameters: date, agent_id, amount_sent).
@app.route("/payment/out/", methods=["POST"])
def addOutgoingPayment():
    date = request.args.get('date', default="", type=str)
    agent_id = request.args.get('agent_id', default="", type=str)
    amount_sent = request.args.get('amount_sent', default=-1, type=float)

    if (date==""):
        return jsonify(success=False, message="Invalid payment date")

    if (amount_sent<0):
        return jsonify(success=False, message="Invalid amount")

    if (company.getAgentById(agent_id)==None):
        return jsonify(success=False, message="Agent not found")

    company.addPayment("OUT", date, agent_id, amount_sent)
    return jsonify(success=True, message="Added an outgoing payment successfuly.")

#Return a list of all incoming and outgoing payments.
@app.route("/payments/", methods=["GET"])
def allPayments():
    return jsonify(payments=[p.serialize() for p in company.payments])


# Stats HTTP Methods

# Return a list of all claims, grouped by responsible agents
@app.route("/stats/claims", methods=["GET"])
def allClaimsGroupedByAgents():
    """ Returns a dictionary mapping an agent_id to a list of claims. """
    data = dict()
    for claim in company.claims:
        # get the assigned agent to that customer
        agent = company.getAssignedAgent(claim.customer_id)
        # customer is not assigned to any agent, skip this claim
        if (agent==None):
            continue

        data[agent.ID] = data.get(agent.ID, [])
        data[agent.ID].append(claim.serialize())

    return jsonify(claims=data)

#Return a list of all revenues, grouped by responsible agents
@app.route("/stats/revenues", methods=["GET"])
def allRevenuesGroupedByAgents():
    payments = [p for p in company.getPayments() if p.payment_type=="OUT"]
    data = dict()
    for payment in payments:
        agent_id = payment.payer_id
        data[agent_id] = data.get(agent_id, [])
        data[agent_id].append(payment.serialize())

    return jsonify(revenues=data)

#Return a sorted list of agents based on their performance.
@app.route("/stats/agents", methods=["GET"])
def allAgentsSortedByPerformance():
    # performance is based on the total revenues for the agent and the number of customers as well
    agents = company.getAgents()

    # add the number of customers to each agent's performance
    performance = {agent.ID:len(agent.customers) for agent in agents}

    # add the total revenues for each agent to each agent's performance
    for payment in company.getPayments():
        if (payment.payment_type=="OUT"):
            performance[payment.payer_id] += payment.amount

    # the list is sorted from the best to the worst agent
    agents.sort(key=lambda agent: performance[agent.ID], reverse=True)

    return jsonify(agents=[a.serialize() for a in agents])


###DO NOT CHANGE CODE BELOW THIS LINE ##############################
@app.route("/")
def index():
    return jsonify(
            success = True,
            message = "Your server is running! Welcome to the Insurance Company API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)
