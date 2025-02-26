import zmq
import pandas as pd

# Initialize ZeroMQ context
context = zmq.Context()
a_socket = context.socket(zmq.REP)
port = "tcp://*:30000"
a_socket.bind(port)  # Microservice A listens on port 30000
print("Microservice A is running and waiting for reservation requests...")
RESERVATION_DATA = "../csv/reservation_data.csv"  # Path to the CSV file


def validate_received_json(requests):
    """
    Validates the JSON request structure
    :param requests: JSON input
    :return: error if request was incorrect
    """
    if not isinstance(requests, dict) or "request" not in requests:
        return {"error": "Invalid Request Format"}

    event = requests["request"].get("event")
    body = requests["request"].get("body", {})

    if event != "reservationData" or "customerName" not in body:
        return {"error": "Invalid request event or missing customerName"}

    return None  # No errors


def construct_response_json(customer):
    """
    Reads reservation CSV and filters by customer name.
    Constructs JSON response
    :param customer: Customer's name to construct JSON response with
    :return: Reservation Data
    """
    try:
        df = pd.read_csv(RESERVATION_DATA, encoding="utf-8")
        res_cus = df[df["Name"].str.strip() == customer]
        # If user enters incorrect customer name
        if res_cus.empty:
            return {"error": f"No reservations found for customer {customer}"}
        res_his = res_cus[["Date", "Time", "Number"]].to_dict(orient="records")
    except FileNotFoundError:
        return {"error": "Reservation data file not found"}

    return {
        "response": {
            "event": "reservationData",
            "body": {
                "customerName": customer,
                "history": res_his if res_his else []
            }
        }
    }


def send_error_response(socket: object, error_message: str) -> dict:
    """
    Sends a properly formatted error response.
    :rtype: str
    :param socket: port listening on
    :param error_message: JSON response
    """
    return {
        "response": {
            "event": "reservationData",
            "body": {
                "error": error_message,
                "history": []
            }
        }
    }


def respond_json(socket, responses):
    socket.send_json(responses)
    print(f"Response sent was: {responses}")


while True:
    request = a_socket.recv_json()

    # Validate request
    error = validate_received_json(request)
    if error:
        respond_json(a_socket, send_error_response(a_socket, error["error"]))
        continue

    # Process request
    cus_name = (
        request.get("request", {}).get("body", {}).get("customerName", "")
    )
    response = construct_response_json(cus_name)

    # Handle potential file errors
    if "error" in response:
        respond_json(
            a_socket, send_error_response(a_socket, response["error"])
        )
        continue

    # Send successful response
    respond_json(a_socket, response)

