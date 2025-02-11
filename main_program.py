# ONID: walshand
# Andrew Walsh
# 2/10/2025
#
#
import json

import zmq
'''
TODO LIST
- Task management system: Jira
- Write unit testing
'''


def connect():
    """
    Initialize ZeroMQ environment and connect to server.
    :return: socket
    """
    # set up env and create socket
    context = zmq.Context()
    # Request socket -> Reply socket (.REP)
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    return socket


def calculation_request(socket, project):
    """
    Sends requests to the microservice and receives response.
    :param socket: ZeroMQ socket
    :param project: Sod, Retaining wall, or labor costs
    """
    print(f"Sending request for {project} calculation...")
    socket.send_string(project)        # Send project to server
    response = socket.recv().decode()  # Receive result
    print(f"Calculation result: {project}\n")


def sod(socket):
    """
    Handles Sod UI and Calculation requests
    :param socket:  ZeroMQ socket
    """

    while True:
        print("\n[Sod Installation Calculator]")
        print("1. To Sod Installation information")
        print("2. Project Folder")
        print("Q. <- Go Back <-")

        choice = input("Enter a number or Q: ").strip().upper()
        if choice == "Q":
            break
        elif choice == "1":
            print("Enter lawn size in square feet (Length X Width): ")
            length = input("Length: ")
            width = input("Width: ")
            socket.send(f"Sod {length, width}")
            response = socket.recv().decode()
            print(f"Sod Installation cost: {response}")
        elif choice == "2":
            folder(socket)
        else:
            print("Invalid input, please try again.")


def wall(socket):
    """
    Handles retaining wall UI and Calculation requests
    :param socket:  ZeroMQ socket
    """
    while True:
        print("\n[Retaining Wall Calculator]")
        print("1. To Enter Retaining Wall information")
        print("2. Project Folder")
        print("Q. <- Go Back <-")

        choice = input("Enter a number or Q: ").strip().upper()
        if choice == "Q":
            break
        elif choice == "1":
            print("Enter desired wall size in square feet (Length X height): ")
            length = input("Length: ")
            height = input("Height: ")
            socket.send(f"Sod {length, height}")
            response = socket.recv().decode()
            print(f"Retaining Wall cost: {response}")
        elif choice == "2":
            folder(socket)
        else:
            print("Invalid input, please try again.")


def labor(socket):
    """
    Handles labor and Calculation requests
    :param socket:  ZeroMQ socket
    """
    labor_data = {
        "Worker": (0, 0.0),
        "Crew Lead": (0, 0.0),
        "Supervisor": (0, 0.0),
    }

    while True:
        print("\n[Manage workers]")
        print("1. To enter workers information")
        print("2. Project Folder")
        print("Q. <- Go Back <-")

        choice = input("Enter a number or Q: ").strip().upper()

        if choice == "Q":
            break
        elif choice == "1":
            while True:
                print("\nEnter worker details:")
                print("Roles: Worker, Crew Lead, Supervisor")
                # User picks a role then enters quantity for role
                role = input("Role: ").strip().title()

                if role not in labor_data:
                    print("Invalid Role. Please enter Worker, Crew Lead, or Supervisor.")
                    continue

                try:
                    quantity = int(input(f"Enter quantity of {role}s: ").strip())
                    wage = float(input(f"Enter hourly wage for {role}: $").strip())
                    # Add input to labor_data dictionary
                    labor_data[role] = (quantity, wage)
                except ValueError:
                    print("Invalid input, please try again.\n")
                    continue

                more = input("Do you want to enter another role? (Y/N): ").strip().upper()
                if more != "Y":
                    ui(socket)

            # Send labor_data as JSON
            socket.send_string(json.dumps({"Labor": labor_data}))
            response = socket.recv().decode()
            print(f"Total Labor Cost: {response}")

        elif choice == "2":
            folder(socket)
        else:
            print("Invalid input, please try again.\n")


def folder(socket):
    """
    Brings user to their project folder
    :param socket: ZeroMQ socket
    """
    while True:
        print("\n[Project Folder]")
        break


def ui(socket):
    """
    ==Main Menu==
    Receives user input for which project they want to calculate
    :param socket
    """
    while True:
        print("\nWhich project would you like to calculate first?")
        print("1. Sod installation")
        print("2. Retaining wall installation")
        print("3. Manage workers")
        print("4. Project Folder")
        print("Q. to quit the program")

        choice = input("Enter which project to calculate: ").strip().upper()

        if choice == "Q":
            print("Goodbye!")
            exit()
        elif choice == "1":
            sod(socket)
        elif choice == "2":
            wall(socket)
        elif choice == "3":
            labor(socket)
        elif choice == "4":
            folder(socket)
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    print("\n[Welcome to Landscape Calculator!]\n")
    print("This program can calculate different landscape projects and allows you to save to your Project Folder.")
    print("There you can manage and edit your projects and see total costs.")
    print("You can also do project management by adjusting your labor costs and worker wages.\n")

    socket = connect()
    ui(socket)
