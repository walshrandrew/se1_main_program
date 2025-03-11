import csv
import zmq

# Initialize ZeroMQ context
context = zmq.Context()
d_socket = context.socket(zmq.REP)
d_socket.bind("tcp://*:5558")

print("Microservice D is running and waiting for reservation requests...")
file_name = '../csv/labors_data.csv'


def get_crew_list():
    # Get unique crew names
    crew_list = set()
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            crew_list.add(row['crewName'])
    return list(crew_list)


def edit_crew(crew_name, crew_type, new_num, new_wage):
    rows = []
    with open(file_name, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['crewName'] == crew_name and row['type'] == crew_type:
                row['num'] = str(new_num)
                row['wage'] = str(new_wage)
            rows.append(row)

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['crewName', 'type', 'num', 'wage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def delete_crew(crew_name):
    rows = []
    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['crewName'] != crew_name:  # Skip rows that match the crew_name to delete
                rows.append(row)

    # Rewrite the CSV file without the deleted crew
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['crewName', 'type', 'num', 'wage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{crew_name} deleted Successfully")


while True:
    request = d_socket.recv_json()
    print(f"Received request: {request}")
    event = request.get("request").get("event")
    print(f"Received event: {event}")
    crew_name = request.get("request", {}).get("body", {}).get("crewName")
    print(f"Received crew name: {crew_name}")

    if event == "getCrewList":
        crew_list = get_crew_list()
        d_socket.send_json({"crew_list": crew_list})
        continue

    elif event == "editCrew":
        body = request.get("request", {}).get("body", {})  # Safe way to retrieve the body dictionary
        crew_name = body.get("crewName")
        crew_type = body.get("crew_type")
        new_num = body.get("new_num")
        new_wage = body.get("new_wage")
        edit_crew(crew_name, crew_type, new_num, new_wage)
        d_socket.send_json({"message": f"Crew '{crew_name}' edited successfully!"})
        continue

    elif event == "deleteCrew":
        delete_crew(crew_name)
        d_socket.send_json({"response": {"event": "deleteCrew", "code": "200"}})
        continue
