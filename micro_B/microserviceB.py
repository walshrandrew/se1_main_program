import zmq
import csv
import json

context = zmq.Context()
b_socket = context.socket(zmq.REP)
b_socket.bind("tcp://*:5556")

sod_file = '../csv/sod_project.csv'
labor_file = '../csv/labors_data.csv'
last_project_details = None

print("Microservice B is running and waiting for requests...")


def calculate_project_cost(data):
    """
    Calculates the total project cost.

    Process:
    - Extract parameters: sod_variety, crew (crewName), project_duration, material_cost.
    - Read 'labors_data.csv' (format: crewName,type,num,wage) and sum labor cost for matching crew.
      Matching is done if the CSV crewName (lowercase) is found in the provided crew name (lowercase).
    - Compute total labor cost as: sum_labor * duration.
    - Compute total project cost as: total_labor_cost * material_cost.
    """
    try:
        body = data["request"]["body"]
        sod_variety = body["sod_variety"]
        crew = body["crewName"]
        duration = float(body["project_duration"])
        material_cost = float(body["material_cost"])
    except Exception as e:
        return {"error": "Invalid request data: " + str(e)}

    sum_labor = 0.0
    try:
        with open(labor_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_crew = row.get('crewName', '').strip().lower()
                provided_crew = crew.strip().lower()
                # If the CSV crew name is contained within the provided crew name, consider it a match.
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

    # Save details for potential later saving.
    global last_project_details
    last_project_details = {
        "sod_variety": sod_variety,
        "crew": crew,
        "project_duration": duration,
        "project_total_cost": total_project_cost
    }

    return {"total_project_cost": total_project_cost}


def save_project():
    """
    Saves the last project details into 'sod_projects.csv'.
    Expected CSV columns: sod_variety,crew,project_duration,project_total_cost
    """
    global last_project_details
    if not last_project_details:
        return {"error": "No project details available to save."}

    try:
        with open(sod_file, 'a', newline='') as csvfile:
            fieldnames = ["sod_variety", "crew", "project_duration", "project_total_cost"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not sod_file:
                writer.writeheader()
            writer.writerow(last_project_details)
    except Exception as e:
        return {"response": {"code": "500", "message": "Save failed: " + str(e)}}

    return {"response": {"code": "200", "message": "Project saved successfully."}}


while True:
    try:
        message = b_socket.recv()
        try:
            # Attempt to decode the message as JSON.
            data = json.loads(message.decode('utf-8'))
        except Exception:
            # If decoding fails, treat the message as a plain string (save request).
            data = message.decode('utf-8')

        if isinstance(data, dict) and "request" in data:
            event = data["request"].get("event")
            if event == "getSodCalc":
                response = calculate_project_cost(data)
                b_socket.send_json(response)
            elif event == "postSodCalc":
                response = save_project()
                b_socket.send_json(response)
            else:
                b_socket.send_json({"error": "Unknown event"})

    except Exception as e:
        error_response = {"error": str(e)}
        b_socket.send_json(error_response)
