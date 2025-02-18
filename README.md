# se1_main_program
Main program for Software Engineering 1
# Landscape Project Calculator

This project involves creating a system that interacts with multiple microservices to calculate the cost of different landscape project options. The main program communicates with a server, which in turn interacts with microservices to calculate labor and material costs for tasks such as sod installation and retaining wall installation.

## Project Structure

- **main_program.py**: Entry point where the user provides inputs, such as crew names, labor quantities, and hourly rates.
- **server.py**: Main program that handles communication with microservices and manages requests.
- **microserviceA.py**: Microservice that calculates labor costs based on provided crew data.


## Requirements

- Python 3.x
- ZeroMQ (`zmq` library) for messaging

## Setup

1. Install the required dependencies:
   pip install pyzmq
   
Ensure that you have the following files in your project:
server.py: Main server script.
microserviceA.py: Microservice that performs labor cost calculations.
main_program.py: Script where users input data.  

How it Works
Main Program:

Users enter crew names and labor information (such as roles and hourly rates).
This data is sent to server.py which forwards it to microserviceA.py.

Server:
The server listens on a specific port (5000) for incoming labor data.
The server forwards this data to microserviceA.py, which listens on port 5556.

Microservice A:
Microservice A receives the labor data, calculates the total labor cost, and sends the results back to the server.

Response:
The server receives the response from microservice A and sends it back to the main program.

Example of Data Flow
User Input (main program): -> server -> Microservices -> server -> main program

## Shinji's Microservice A
**HOW TO REQUEST DATA**
- Connect to PORT:30000
- Enter Customer information
- send a JSON request with socket.send_json(request_reservation_json)
```javascript{
request_reservation_json = {  
  "request": {  
     "event": "reservationData",  
     "body": {  
     "customerName": customer_name  
     }  
  }  
}  
}  
========================================================================
  
**HOW TO RECEIVE DATA**
- Receive JSON data with receive_reservation_json = socket.recv_json()
- Validate request structure contains "request"
- Validate event is "reservationData"
- Reads reservation CSV and filters by customer name
- Sends back {response} with a_socket.send_json(response)
```javascript{
response = {  
  "response": {  
  "event": "reservationData",  
  "body": {  
     "customerName": customer_name,  
     "history": reservation_history  
     }  
  }  
}  
}  
========================================================================
  
**UML**




