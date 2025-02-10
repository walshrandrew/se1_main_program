'''
TODO LIST
- Task management system: Jira
- Write unit testing
'''


class Projects:
    def __init__(self, sod, wall, labor):
        self.sod = sod
        self.wall = wall
        self.labor = labor


def verify_project():
    """
    Receives user input for which project they want to calculate
    :param user_input:
    :return: project name
    """
    choice = input("Enter which project to calculate with a number [1-3]: \n")
    if choice == "Q":
        print("Goodbye!")
        exit()
    while True:
        try:
            choice = int(input("Enter which project to calculate with a number [1-3]: \n"))

            if 1 <= choice <= 3:
                if choice == 1:
                    return "Sod installation"
                if choice == 2:
                    return "Retaining wall installation"
                if choice == 3:
                    return "Manage worker wages"
            else:
                print("Invalid Input. Please try again.\n")
                print("1. Sod installation")
                print("2. Retaining wall installation")
                print("3. Manage worker wages")

        except ValueError:
            print("Invalid Input. Please try again.\n")
            print("1. Sod installation")
            print("2. Retaining wall installation")
            print("3. Manage worker wages")


print("Welcome to Landscape Calculator!\n")
print("This program can calculate different landscape projects and allows you to save to your Project Folder.")
print("There you can manage and edit your projects and see total costs.")
print("You can also do project management by adjusting your labor costs and worker wages.\n")
print("Which project would you like to calculate first?")
print("1. Sod installation")
print("2. Retaining wall installation")
print("3. Manage worker wages")
print("Q. to quit the program")

user_input = verify_project()
print(f"You selected {user_input}.")



