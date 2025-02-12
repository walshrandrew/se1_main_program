import zmq
import json
'''
test
'''
# Initialize ZeroMQ context
context = zmq.Context()

# Create a REP socket to receive requests from server.py
a_socket = context.socket(zmq.REP)
a_socket.bind("tcp://*:5556")  # Microservice A listens on port 5555

print("Microservice A is running and waiting for labor package...")

while True:
    # Receive labor data from server.py
    labor_package = a_socket.recv_json()
    print(f"Microservice A received labor data: {labor_package}")