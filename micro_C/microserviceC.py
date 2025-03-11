import zmq

# Retaining wall Calculator
# Receives request from server.py on 5557
# Server.py will send labor data too
# Retaining wall will calculate the project installation cost with specified crew
# microserviceC sends that data back to server.py
# server.py forwards that to the Retaining wall page.

# Initialize ZeroMQ context
context = zmq.Context()
c_socket = context.socket(zmq.REP)
c_socket.bind("tcp://*:5557")

print("Microservice C is running and waiting for reservation requests...")