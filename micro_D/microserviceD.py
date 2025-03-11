import csv

import zmq

# My Folder microservice D
# opens CSV file for editing
# opens CSV file for deleting crew info
# DO NOT DELETE THE HEADER!!!

# First receive JSON request from server.py
# If request is for editing
# open csv file for editing (how do I do that?)
# If request is for deleting data
# Delete specified crew


# Initialize ZeroMQ context
context = zmq.Context()
d_socket = context.socket(zmq.REP)
d_socket.bind("tcp://*:5558")

print("Microservice D is running and waiting for reservation requests...")


def get_crew_list():
    # Get unique crew names
    crew_list = set()
    with open('labors_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            crew_list.add(row['crewName'])
    return list(crew_list)


def edit_crew(crew_name, crew_type, new_num, new_wage):
    rows = []
    with open('labors_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['crewName'] == crew_name and row['type']:
                row['num'] = str(new_num)
                row['wage'] = str(new_wage)
            rows.append(row)

    with open('labors_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['crewName', 'crew_data']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(rows)


def delete_crew(crew_name):
    rows = []
    with open('labors_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['crewName'] != crew_name:
                rows.append()


while True:
    request = d_socket.recv_json()
    print(f"Received request: {request}")

    if request.get("event") == "getCrewList":
        crew_list = get_crew_list()
        d_socket.send_json({"crew_list": crew_list})
        continue

    elif request.get("event") == "editCrew":
        crew_name = request["body"]["crewName"]
        crew_type = request["body"][""]
        new_data = request["body"]["new_data"]
        edit_crew(crew_name, new_data)
        d_socket.send_json({"message": f"Crew '{crew_name}' edited successfully!"})
        continue

    elif request.get("event") == "deleteCrew":
        crew_name = request["body"]["crewName"]
        delete_crew(crew_name)
        d_socket.send_json({"message": f"Crew '{crew_name}' deleted successfully!"})
        continue
