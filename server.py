import time
import zmq # For zeroMQ

# context sets up environment so we can create sockets
context = zmq.Context()
# REP is reply socket
main_socket = context.socket(zmq.REP)
# Address string. This is where socket listens on network port.
main_socket.bind("tcp://*:5000")

a_socket = context.socket(zmq.REQ)
a_socket.connect("tcp://localhost:5555")  # connect to microservice A

b_socket = context.socket(zmq.REQ)
b_socket.connect("tcp://localhost:5556")  # connect to microservice A

c_socket = context.socket(zmq.REQ)
c_socket.connect("tcp://localhost:5557")  # connect to microservice A

print("Server listening...")

# loop to listen for message from client.
while True:
    # Receive labor data from main
    request = main_socket.recv_json()
    print(f"Received request from main program: {request}")
    # Read JSON data package for event type like getLaborCost
    service = request.get("event")

    # Request microservice A to get labor cost
    if service == "getLaborCost": # total labor cost X duration
        a_socket.send_json(request)
        print(f"Forwarding {request} to microservice A")
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")

    elif service == "getLaborData": # Reads CSV file for labor data
        a_socket.send_json(request)
        print(f"Forwarding {request} to microservice A")
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")

    elif service == "postLaborData": # Writes to CSV file for labor data (will call this when user inputs labor data)
        a_socket.send_json(request)
        print(f"Forwarding {request} to microservice A")
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")

    # Request microservice B to ...

    # Request microservice C to ...
    else:
        print("Invalid Request Received...")
        continue

    # Send what you got back to main
    main_socket.send_json(response)