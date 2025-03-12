import zmq
import csv
import json
import os

context = zmq.Context()
c_socket = context.socket(zmq.REP)
c_socket.bind("tcp://*:5577")

wall_file = '../csv/rw_project.csv'
labor_file = '../csv/labors_data.csv'
last_project_details = None

print("Microservice C is running and waiting for requests...")


def calculate_project_cost(data):
    """
    Calculates RW project costs.
    """
    try:
        body = data["request"]["body"]
        rw_variety = body["rw_variety"]
        crew = body["crewName"]
        duration = float(body["project_duration"])
        material_cost = float(body["material_cost"])
    except Exception as e:
        print("Error in parsing request data:", e)
        return {"error": "Invalid request data: " + str(e)}

    sum_labor = 0.0
    try:
        with open(labor_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_crew = row.get('crewName', '').strip().lower()
                provided_crew = crew.strip().lower()

                if csv_crew in provided_crew:
                    try:
                        num = float(row.get('num', 0))
                        wage = float(row.get('wage', 0))
                        sum_labor += num * wage
                    except ValueError:
                        continue
    except Exception as e:
        return {"error": "Failed to read labors_data.csv: " + str(e)}

    total_labor_cost = sum_labor * duration
    total_project_cost = total_labor_cost + material_cost

    global last_project_details
    last_project_details = {
        "rw_variety": rw_variety,
        "crew": crew,
        "project_duration": duration,
        "project_total_cost": total_project_cost
    }
    return {"total_project_cost": total_project_cost}


def save_project():
    global last_project_details
    if not last_project_details:
        return {"error": "No project details available to save."}

    try:
        with open(wall_file, 'a', newline='') as csvfile:
            fieldnames = ["rw_variety", "crew", "project_duration", "project_total_cost"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write header if file is empty or does not exist
            if not wall_file:
                writer.writeheader()
            writer.writerow(last_project_details)
    except Exception as e:
        print("Save failed:", e)
        return {"response": {"code": "500", "message": "Save failed: " + str(e)}}

    print("Save successful...")
    return {"response": {"code": "200", "message": "Project saved successfully."}}


while True:
    try:
        message = c_socket.recv()
        try:
            # Attempt to decode the message as JSON.
            data = json.loads(message.decode('utf-8'))
        except Exception:
            # If decoding fails, treat the message as a plain string (save request).
            data = message.decode('utf-8')

        if isinstance(data, dict) and "request" in data:
            event = data["request"].get("event")
            if event == "getRWCalc":
                response = calculate_project_cost(data)
                c_socket.send_json(response)
            elif event == "postRWCalc":
                response = save_project()
                c_socket.send_json(response)
            else:
                c_socket.send_json({"error": "Unknown event"})
        else:
            c_socket.send_json({"error": "Invalid request format"})

    except Exception as e:
        error_response = {"error": str(e)}
        c_socket.send_json(error_response)
