# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime


def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")
        
        while new_username in username_password.keys():
            print(f'{new_username} already exists. Please try another one.')
            return
       
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
    # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
                
    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")

task_list = []

def add_task():
    global task_list

    # Request input of a new task
    task_username = input("Name of person assigned to task: ")

    # Check if the user is in the dictionary
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # If the user exists, request more info about the task
    while True:
        try:
            due_date = input("Due date of task (YYYY-MM-DD): ")
            task_due_date = due_date.split("-")
            task_due_date = list(map(lambda x: int(x), task_due_date))
            due_date = "-".join(map(str, task_due_date))
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = datetime.today().date()
    
    # Add all the details to the task list
    new_task = f"{task_username};{task_title};{task_description};{due_date};{curr_date.strftime('%Y-%m-%d')};No"
    task_list.append(new_task)

    # Write the updated task list to the tasks.txt file
    with open("tasks.txt", "w") as task_file:
        for task in task_list:
            task_file.write(task + "\n")
        print("Task successfully added.")

# Display all tasks in the task list
def view_all():
    global task_list

    if not task_list:
        print("No tasks to display.")
        return

    else:
        print()
        for task in task_list:
            tasks_unit = task.split(';')
            disp_str = f"Task: \t\t {tasks_unit[1]}\n"
            disp_str += f"Assigned to: \t {tasks_unit[0]}\n"
            disp_str += f"Date Assigned: \t {tasks_unit[4]}\n"
            disp_str += f"Due Date: \t {tasks_unit[3]}\n"
            disp_str += f"Task Description: \n {tasks_unit[2]}\n"
            print(disp_str)
            print('-' * 80)

# Display tasks assigned to the current user
def view_mine():
    global task_list, curr_user

    user_tasks = [task for task in task_list if task.split(';')[0] == curr_user]
    print()
    for i, task in enumerate(user_tasks, start=1):
        tasks_unit = task.split(';')
        disp_str = f"Task: \t {tasks_unit[1]}\n"
        disp_str += f"Assigned to: \t {tasks_unit[0]}\n"
        disp_str += f"Date Assigned: \t {tasks_unit[4]}\n"
        disp_str += f"Due Date: \t {tasks_unit[3]}\n"
        disp_str += f"Task Description: \n {tasks_unit[2]}\n"
        print(i, disp_str)
        print('-'*80)

    # Allow the user to select a task        
    while True:
        user_choice = input('Enter the number of the task you want to select (or -1 to return to menu): ')
        if user_choice == '-1':
            return
        user_choice = int(user_choice)
        if 1 <= user_choice <= len(user_tasks): 
            user_task = user_tasks[user_choice - 1]
            break
        else:
            print("Invalid task number. Please try again.")
    
    tasks_unit = user_task.split(';')

    # Allow the user to mark the task as complete or to edit the task

    while True:
        action = input('Select an action (mark as complete/ edit task): ').lower()
        if action == 'mark as complete':
            tasks_unit[5] = "Yes"
            print("Task marked as complete.")
            print()
            break
        elif action == 'edit task':
            if tasks_unit[5] == "No":
                edit_username = input('Enter the new username: ')
                if edit_username:
                    tasks_unit[0] = edit_username
                edit_due_date = input('Enter the new due date (YYYY-MM-DD): ')
                if edit_due_date:
                    tasks_unit[3] = edit_due_date
                    print("Task edited successfully.")
                    break
            else:
                print("Completed tasks cannot be edited.")
                break
        else:
            print("Invalid action. Please try again.")

    # Update the task in the task list
    updated_task = ";".join(tasks_unit)
    task_list[task_list.index(user_task)] = updated_task

    # Write the updated task list to the tasks.txt file
    with open("tasks.txt", "w") as task_file:
        for task in task_list:
            task_file.write(task + "\n")
    print("Task successfully updated.")

# convert the due_date to an object
def due_date_obj(due_date):
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    return due_date_obj

def reports():
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task.split(';')[5] == "Yes")
    uncompleted_tasks = total_tasks - completed_tasks
    now = datetime.today().date()
    overdue_tasks = sum(1 for task in task_list if task.split(';')[5] == "No" and due_date_obj(task.split(';')[3]) < now)
    
    try:
        percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
        percentage_overdue = (overdue_tasks / uncompleted_tasks) * 100

    except ZeroDivisionError:
        percentage_incomplete = 0
        percentage_overdue = 0

    # Write task overview report to task_overview.txt
    with open("task_overview.txt", "w") as overview_file:
        overview_file.write("Task Overview:\n")
        overview_file.write(f"Total number of tasks: {total_tasks}\n")
        overview_file.write(f"Total number of completed tasks: {completed_tasks}\n")
        overview_file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        overview_file.write(f"Total number of overdue tasks: {overdue_tasks}\n")
        overview_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:}%\n")
        overview_file.write(f"Percentage of tasks that are overdue: {percentage_overdue:}%\n")

    total_users = len(username_password)
    total_tasks = len(task_list)

    # Write user overview report to user_overview.txt
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview:\n")
        user_overview_file.write(f"Total number of users registered: {total_users}\n")
        user_overview_file.write(f"Total number of tasks generated and tracked: {total_tasks}\n\n")

        user_tasks = {}
        for user in username_password.keys():
            user_tasks[user] = []
            for task in task_list:
                if task.split(';')[0] == user:
                    user_tasks[user].append(task.split(';'))

            num_user_tasks = len(user_tasks[user])
            total_user_tasks = len(task_list)
            percentage_assigned = (num_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
            completed_user_tasks = sum(1 for task in user_tasks[user] if task[5] == "Yes")
            user_percentage_completed = (completed_user_tasks / num_user_tasks) * 100 if num_user_tasks > 0 else 0
            incompleted_user_tasks = num_user_tasks - completed_user_tasks
            user_overdue_tasks = sum(1 for task in user_tasks[user] if task[5] == "No" and due_date_obj(task[3]) < now)
            percentage_incomplete = (incompleted_user_tasks / num_user_tasks) * 100 if num_user_tasks > 0 else 0
            percentage_overdue = (user_overdue_tasks / num_user_tasks) * 100 if num_user_tasks > 0 else 0

            user_overview_file.write(f"User: {user}\n")
            user_overview_file.write(f"Total number of tasks assigned: {num_user_tasks}\n")
            user_overview_file.write(f"Percentage of total tasks assigned: {percentage_assigned:.2f}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {user_percentage_completed:.2f}%\n")
            user_overview_file.write(f"Percentage of incomplete tasks: {percentage_incomplete:.2f}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n\n")

    print("Task overview report generated successfully.")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_list = task_file.read().split("\n")
    task_list = [t for t in task_list if t != ""]
    
#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
        # if ';' in user_data:
        username, password = user.split(';')
        username_password.update({username : password})
        
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user in username_password.keys() and username_password[curr_user] == curr_pass:
        print("Login Successful!")
        logged_in = True
    else:
        print("Invalid username or password. Please try again.")


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
        
    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        reports()    
                   
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        
        # Check if tasks.txt and user.txt exist, if not, generate them
        if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
            reg_user()
            add_task()

        # Read task data from tasks.txt
        with open("tasks.txt", "r") as task_file:
            task_data = task_file.readlines()

        total_tasks = len(task_data)
        completed_tasks = sum(1 for task in task_data if task.split(";")[-1].strip() == "Yes")
        incomplete_tasks = total_tasks - completed_tasks 

        # Read user data from user.txt
        with open("user.txt", "r") as user_file:
            user_data = user_file.readlines()

        total_users = len(user_data)
        
        # Display statistics
        print("-----------------------------------")
        print("Statistics Overview:")
        print(f"Total number of users: {total_users}")
        print(f"Total number of tasks: {total_tasks}")
        print(f"Number of completed tasks: {completed_tasks}")
        print(f"Number of incomplete tasks: {incomplete_tasks}")
        print("-----------------------------------")   

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")