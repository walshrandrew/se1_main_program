# ONID: walshand
# Andrew Walsh
# 2/10/2025
# Landscape Calculator


import json
import zmq


def connect():
    """
    Initialize ZeroMQ environment and connect to server.
    :return: socket
    """
    # set up env and create socket
    context = zmq.Context()
    # Request socket -> Reply socket (.REP)
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5000")
    return socket


def sod(socket):
    """
    ==Sod Calculator Sub Menu==
    Handles Sod UI and Calculation requests
    :param socket:  ZeroMQ socket
    """

    sod_data = {
        "Kentucky Blue": 1.52,
        "Perennial Rye": 1.5,
        "Bahia": 1.32,
        "Buffalo": 1.3,
        "Carpet": 1.28,
        "Fine Fescue": 1.26,
        "Fescue Mix": 1.20,
        "Centipede": 1.01,
        "St. Augustine": .98,
        "Zoysia": .93,
        "Bermuda": .92
    }

    while True:
        print("\n[Sod Installation Calculator]")
        print("1. To Sod Installation information")
        print("2. Project Folder")
        print("Q. <- Go Back <-")

        choice = input("Enter a number or Q: ").strip().upper()
        if choice == "Q":
            break
        elif choice == "1":
            while True:
                print("\n[Select Sod Variety")
                print("Kentucky Blue: $1.52, Perennial Rye: $1.5, Bahia: $1.32, Buffalo: $1.3")
                print("Carpet: $1.28, Fine Fescue: $1.26, Fescue Mix: $1.20, Centipede: $1.01,")
                print("St. Augustine: $0.98, Zoysia: $0.93, Bermuda: $0.92")
                # User input sod variety
                variety = input("Enter Sod Variety: ")
                # Error handler
                if variety not in sod_data:
                    print("Invalid sod variety, please try again.\n")
                    continue
                # Take user square footage
                try:
                    print("Enter lawn size in square feet (Length X Width): ")
                    length = float(input("Lawn Length (feet): "))
                    width = float(input("Lawn Width (feet): "))
                    area = length * width
                    cost = area * sod_data[variety]
                except ValueError:
                    print("Invalid input, please try again.\n")
                    continue

                print(f"This is your total for materials: ${cost}")
                save = input(f"Would you like to save this sod project? (Y/N): ").strip().upper()
                if save != "Y":
                    return
                else:
                    print("Sending to Project Folder...")
                    socket.send_string(json.dumps({"Sod": sod_data}))
                    response = socket.recv().decode()
                    print(f"Total Sod Cost with labor included: {response}")
                    return

        elif choice == "2":
            folder(socket)
        else:
            print("Invalid input, please try again.")


def wall(socket):
    """
    ==Retaining Wall Sub Menu==
    Handles retaining wall UI and Calculation requests
    :param socket:  ZeroMQ socket
    """

    wall_data = {
        "Cinder": 2,
        "Small": 3,
        "Interlocking Concrete": 4,
        "Large": 6,
        "Boulder Rock": 15
    }

    while True:
        print("\n[Retaining Wall Installation Calculator]")
        print("1. To Retaining Wall Installation information")
        print("2. Project Folder")
        print("Q. <- Go Back <-")

        choice = input("Enter a number or Q: ").strip().upper()
        if choice == "Q":
            break
        elif choice == "1":
            while True:
                print("\n[Select Retaining Wall Variety")
                print("Cinder: $2, Small: $4, Interlocking Concrete: $4, Large: $6, Boulder Rock: $15")
                # User input sod variety
                variety = input("Enter Retaining Wall Variety: ")
                # Error handler
                if variety not in wall_data:
                    print("Invalid Retaining Wall variety, please try again.\n")
                    continue
                # Take user square footage
                try:
                    print("Enter Retaining Wall dimensions (Length X Height): ")
                    length = float(input("Wall Length (feet): "))
                    height = float(input("Wall Height (feet): "))
                    area = length * height
                    cost = area * wall_data[variety]
                except ValueError:
                    print("Invalid input, please try again.\n")
                    continue

                print(f"This is your total for materials: ${cost}")
                save = input(f"Would you like to save this retaining wall project? (Y/N): ").strip().upper()
                if save != "Y":
                    return
                else:
                    print("Sending to Project Folder...")
                    socket.send_string(json.dumps({"Wall": wall_data}))
                    response = socket.recv().decode()
                    print(f"Total Retaining Wall cost with labor included: {response}")
                    return

        elif choice == "2":
            folder(socket)
        else:
            print("Invalid input, please try again.")


def labor(socket):
    """
    ==Labor Sub Menu==
    Handles labor and Calculation requests
    :param socket:  ZeroMQ socket
    """

    labor_data = {
        "Worker": (0, 0.00),
        "Crew Lead": (0, 0.00),
        "Supervisor": (0, 0.00),
    }

    while True:
        print("\n[Crew Manager]")
        print("1. To enter workers information")
        print("2. Project Folder")
        print("Q. <- Go Back <-")

        # User Navigation
        choice = input("Enter a number or Q: ").strip().upper()
        if choice == "Q":
            break

        elif choice == "1":
            # User inputs Crew Name
            while True:
                print("\n[Crew details]")
                print("Welcome to your Crew manager. First, Assign a crew name, then assign your crew roles.")
                crew_name = input("Enter Crew Name: ").strip()
                if not crew_name:
                    print("Invalid Crew Name, please enter a name.")
                    return

                # Crew Name gets stored in labor_package Dictionary
                labor_package = {
                    "Crew Name": crew_name,
                    "Labor": labor_data
                }

                while True:
                    print("\nRoles: Worker, Crew Lead, Supervisor")

                    # User picks a role then enters quantity for role
                    role = input("Role: ").strip().title()

                    if role not in labor_data:
                        print("Invalid Role. Please enter Worker, Crew Lead, or Supervisor.")
                        continue

                    # User Enters Data
                    try:
                        quantity = int(input(f"Enter quantity of {role}s: ").strip())
                        wage = float(input(f"Enter hourly wage for {role}: $").strip())
                        # Add input to labor_data dictionary
                        labor_data[role] = (quantity, wage)
                    except ValueError:
                        print("Invalid input, please try again.\n")
                        continue

                    # Loop again
                    add_role = input("Do you want to enter another role? (Y/N): ").strip().upper()
                    if add_role != "Y":
                        print("Current Worker information: ", labor_data)
                        save = input(f"Would you like to save this team? (Y/N): ").strip().upper()
                        if save != "Y":
                            return
                        else:
                            # Send request to server.py
                            print("Sending to Project Folder...")
                            socket.send_string(json.dumps(labor_package))
                            response = socket.recv().decode()
                            print(f"Total Labor Cost: {response}")
                            return

        elif choice == "2":
            folder(socket)
        else:
            print("Invalid input, please try again.\n")


def folder(socket):
    """
    == Project Folder Sub-Menu==
    Brings user to their project folder and displays backend data
    :param socket: ZeroMQ socket
    """
    while True:
        print("\n[Project Folder]")
        print("1. View saved labor data")
        print("2. View saved sod calculations")
        print("3. View saved retaining wall calculations")
        print("Q. <- Go Back <-")

        choice = input("Enter a number or Q: ").strip().upper()

        if choice == "Q":
            break
        elif choice == "1":
            socket.send_string("REQUEST_LABOR_DATA") #update
            response = socket.recv().decode()
            print("\n[Saved Labor Data]")
            if not response:
                print("No labor data saved yet")
            else:
                print(f"Crew Name: {response['CrewName']}")
            continue
        elif choice == "2":
            socket.send_string("REQUEST_SOD_DATA") #update
            response = socket.recv().decode()
            print("\n[Saved Sod Calculations]")
            if not response:
                print("No labor data saved yet")
            else:
                print(f"Sod information: {response}")
            continue
        elif choice == "3":
            socket.send_string("REQUEST_WALL_DATA") #update
            response = socket.recv().decode()
            print("\n[Saved Retaining Wall Calculations]")
            if not response:
                print("No labor data saved yet")
            else:
                print(f"Retaining wall information: {response}")
            continue
        else:
            print("Invalid input, please try again.\n")
            continue


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
            sure = input("\nAre you sure you want to quit? (Y/N): ")
            if sure == "Y":
                print("Landscape Calculator Closing")
                exit()
            else:
                continue
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
