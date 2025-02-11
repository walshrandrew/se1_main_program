import time
import zmq # For zeroMQ

# context sets up environment so we can create sockets
context = zmq.Context()
# REP is reply socket
socket = context.socket(zmq.REP)
# Address string. This is where socket listens on network port.
socket.bind("tcp://*:5555")
# loop to listen for message from client.
while True:
    message = socket.recv()
    print(f"Received request from the client: {message.decode()}")
    if len(message) > 0:
        if message.decode() == 'Q': # client asks server to quit
            break

        '''
        Inside this while loop is where the server will handle all client interactions.
        '''
        myString = "This is a message from CS361"
        time.sleep(3)
        # NOTE: if sending a int back you will need to convert it to a string first
        socket.send_string(myString) # send reply back to client as string
# Make a clean exit? (if having bugs check indentation error here)
context.destroy()
