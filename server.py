import time
import zmq  # For zeroMQ

# context sets up environment so we can create sockets
context = zmq.Context()
# REP is reply socket
main_socket = context.socket(zmq.REP)
# Address string. This is where socket listens on network port.
main_socket.bind("tcp://*:5000")

a_socket = context.socket(zmq.REQ)        # Labor data
a_socket.connect("tcp://localhost:5555")  # connect to microservice A

b_socket = context.socket(zmq.REQ)        # Sod calculator
b_socket.connect("tcp://localhost:5556")  # connect to microservice B

c_socket = context.socket(zmq.REQ)        # Retaining wall calculator
c_socket.connect("tcp://localhost:5577")  # connect to microservice C

d_socket = context.socket(zmq.REQ)        # Project management for "My folder"
d_socket.connect("tcp://localhost:5558")  # connect to microservice D

print("Server listening...")

# loop to listen for message from client.
while True:
    # Receive labor data from main
    request = main_socket.recv_json()
    print(f"Received request from main program: {request}")
    # Read JSON data package for event type like getLaborCost
    service = request.get("request").get("event")
    print(f"Event type received: {service}")

    # Request microservice A to get labor cost
    if service == "getLaborCost":  # total labor cost X duration
        print(f"Forwarding {request} to microservice A")
        a_socket.send_json(request)
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")

    elif service == "getLaborData":  # Reads CSV file for labor data
        print(f"Forwarding {request} to microservice A")
        a_socket.send_json(request)
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")

    elif service == "postLaborData":  # Writes to CSV file for labor data (will call this when user inputs labor data)
        print(f"Forwarding {request} to microservice A")
        a_socket.send_json(request)
        response = a_socket.recv_json()
        print(f"Received response from microserviceA {response}")

    # Request microservice B to ...
    elif service == "getSodCalc":
        print(f"Forwarding {request} to microservice B")
        b_socket.send_json(request)
        response = b_socket.recv_json()
        print(f"Received {response} from microservice B")

    elif service == "postSodCalc":
        print(f"Forwarding {request} to microservice B")
        b_socket.send_json(request)
        response = b_socket.recv_json()
        print(f"Received {response} from microservice B")

    # Request microservice C to ...
    elif service == "getRWCalc":
        print(f"Forwarding {request} to microservice C")
        c_socket.send_json(request)
        response = c_socket.recv_json()
        print(f"Received {response} from microservice C")

    elif service == "postRWCalc":
        print(f"Forwarding {request} to microservice C")
        c_socket.send_json(request)
        response = c_socket.recv_json()
        print(f"Received {response} from microservice C")

    # Request microservice D to ...
    elif service == "getCrewList":
        print(f"Forwarding {request} to microservice D")
        d_socket.send_json(request)
        response = d_socket.recv_json()
        print(f"Received {response} from microservice D")

    elif service == "editCrew":
        print(f"Forwarding {request} to microservice D")
        d_socket.send_json(request)
        response = d_socket.recv_json()
        print(f"Received {response} from microservice D")

    elif service == "deleteCrew":
        print(f"Forwarding {request} to microservice D")
        d_socket.send_json(request)
        response = d_socket.recv_json()
        print(f"Received {response} from microservice D")

    else:
        print("Invalid Request Received...")
        continue

    # Send what you got back to main
    main_socket.send_json(response)
