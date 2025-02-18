# Name: Takafumi Suzuki
# OSU Email: suzukt@oregonstate.edu
# Course: CS361
# Assignment: Course Project
# Due Date:
# Description: Driver test module
# version: 0.1

import zmq
import json
from microservice_a.constants import Constants

# create a context and socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://localhost:{Constants.PORT_PDMS}")

# customerAgeData event
with open('customer_age_data_request.json', 'r') as f:
    customer_age_data_request = json.load(f)

with open('customer_age_data_response.json', 'r') as f:
    customer_age_data_response = json.load(f)

# getLaborCost event
with open('total_labor_cost_request.json', 'r') as f:
    total_labor_cost_request = json.load(f)

with open('total_labor_cost_response.json', 'r') as f:
    total_labor_cost_response = json.load(f)

# postLaborCost event
with open('post_labor_data_request.json', 'r') as f:
    post_labor_data_request = json.load(f)

with open('post_labor_data_response.json', 'r') as f:
    post_labor_data_response = json.load(f)

# getLaborCost event
with open('get_labor_data_request.json', 'r') as f:
    get_labor_data_request = json.load(f)

with open('get_labor_data_response.json', 'r') as f:
    get_labor_data_response = json.load(f)

requests = [total_labor_cost_request, post_labor_data_request, get_labor_data_request, customer_age_data_request]
expected = [total_labor_cost_response, post_labor_data_response, get_labor_data_response, customer_age_data_response]

print("[LOG] Launch Driver Service")
i = 0
while True:
    # prepare
    request = json.dumps(requests[i])
    answer = expected[i]

    input("Press any key to send a request: ")

    print(f"[Sent->] {request}")
    socket.send_string(request)

    response = json.loads(socket.recv())
    print(f"[Received<-] {response}")

    assert response == answer, f"[ERROR] Wrong response: {response}, answer: {answer}"
    print("")

    i += 1
    if i == len(requests):
        i = 0

