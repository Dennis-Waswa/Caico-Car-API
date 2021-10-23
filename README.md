# Caico-Car-API
A car insurance API using python and Flask to implement the following functionalities
 Management of customers 
o Add/remove customers to/from the system. Each customer has a customer-id, name, address 
and at least one car associated with the customer number. 
o Add/remove cars to/from customers. Each car has at least the model name, number plate, 
motor power and the year it was manufactured in. 
o Each customer has an insurance agent, who is responsible for him/her. 
 Management of insurance agents 
o Add/remove agents to/from the system. Each agent has an agent-id, name, address. 
o When an agent is removed, transfer all customers in his/her supervision to another 
agent first. 
 Management of insurance claims 
o Customers can file up insurance claims. Such claims are first reviewed by the 
responsible agent and then passed on to the insurance company. Each claim is assigned a 
unique claim-id. 
o Claims are either rejected, partly covered, or fully covered by the insurance policy. 
 Management of financials 
o The system keeps track of the payments made by the customer. 
o Based on the number of customers, and their claims, the agents are paid a monthly 
revenue. 
 Management of general statistics 
o Display total revenue and profits of the insurance company 
o Display claim statistics per customer 
o Display the best agent (customers, claims, …)
