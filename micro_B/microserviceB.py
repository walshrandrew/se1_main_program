import zmq

# Sod Calculator
# Receives request from server.py on 5556
# Server.py will send labor data too
# Sod calculator will calculate the project installation cost with specified crew
# microserviceB sends that data back to server.py
# server.py forwards that to the sod calculator page.

# Initialize ZeroMQ context
context = zmq.Context()
b_socket = context.socket(zmq.REP)
b_socket.bind("tcp://*:5556")

print("Microservice B is running and waiting for reservation requests...")