import json
import zmq
import pandas as pd

# Initialize ZeroMQ context
context = zmq.Context()
a_socket = context.socket(zmq.REP)
a_socket.bind("tcp://*:30000")  # Microservice A listens on port 30000

print("Microservice A is running and waiting for reservation requests...")

RESERVATION_DATA = "../csv/reservation_data.csv"  # Path to the CSV file

while True:
    # Receive JSON request from the main program
    request = a_socket.recv_json()

    # Validate request structure
    if not isinstance(request, dict) or "request" not in request:
        response = {"response": {"error": "Invalid request format"}}
        a_socket.send_json(response)
        continue

    event = request["request"].get("event")
    body = request["request"].get("body", {})

    if event != "reservationData" or "customerName" not in body:
        response = {"response": {"error": "Invalid request event or missing customerName"}}
        a_socket.send_json(response)
        continue

    customer_name = body["customerName"]
    reservation_history = []

    # Read the reservation CSV and filter by customer name
    try:
        df = pd.read_csv(RESERVATION_DATA, encoding="utf-8")
        customer_reservations = df[df["Name"].str.strip() == customer_name]
        reservation_history = customer_reservations[["Date", "Time", "Number"]].to_dict(orient="records")

    except FileNotFoundError:
        response = {"response": {"error": "Reservation data file not found"}}
        a_socket.send_json(response)
        continue

    # Construct response JSON
    response = {
        "response": {
            "event": "reservationData",
            "body": {
                "customerName": customer_name,
                "history": reservation_history
            }
        }
    }

    # Send the JSON response back to the main program
    a_socket.send_json(response)
    print(f"Response sent was: {response}")
