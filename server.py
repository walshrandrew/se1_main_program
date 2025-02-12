import time
import zmq # For zeroMQ

# context sets up environment so we can create sockets
context = zmq.Context()
# REP is reply socket
socket = context.socket(zmq.REP)
# Address string. This is where socket listens on network port.
socket.bind("tcp://*:5000")

a_socket = context.socket(zmq.REQ)
a_socket.connect("tcp://localhost:5556")  # connect to microservice A

print("Server listening...")

# loop to listen for message from client.
while True:
    # Receive labor data from main
    request = socket.recv_json()
    print(f"Received request from main program: {request}")

    # Forward labor data to Micro A
    if request.get("Crew Name", "Labor"):
        labor_package = request.get("Crew Name", "Labor")
        print(f"Forwarding labor data to microserviceA: {labor_package}")
        a_socket.send_json(labor_package)
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")
        socket.send_json(response)
    else:
        print("Invalid request received")

    # Forward data to Micro B
    # Forward data to Micro C
