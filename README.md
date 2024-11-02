# HI GUYS, 🚨NEW PROJECT🚨
# To-do List Project

## Introduction
This project aims to develop a task list using object-oriented programming and the Tkinter library for the graphical interface. By creating this application, I seek to enhance my knowledge in OOP and its practical applications, especially in a job market that values these skills.

## Project Structure
The project is divided into three main files:

1. **Base.py**: This is the database that contains five columns:
   - **Task_id**: An ID generated based on the count of rows in the database.
   - **Object_id**: A column with 5 characters used for task selection.
   - **Name**: The name of the task.
   - **Is_completed**: An indicator that checks if the task is completed or not.
   - **Data_out**: The deadline for completing the task.

### Started Methods
- **fetch_database**: Opens the connection with the cursor.
- **convert_int_to_bool**: Converts the values of 0 or 1 in the is_completed column into booleans.
- **convert_bool_to_int**: Performs the inverse transformation for easier manipulation.
- **close_connection**: Closes the connection and the cursor.

### Functions
- **execute**: Utilizes memory efficiently by opening the connection, executing the task, and closing it afterward.
- **create_base**: Creates the database with the mentioned columns.
- **add_task**: Adds a new task to the database.
- **check_completed**: Checks if the task is completed.
- **recover_task**: Recovers a deleted task.
- **update_task**: Allows the user to modify an existing task.
- **delete_task**: Removes a specific task.
- **delete_all**: Deletes all tasks in the database.
- **search_task**: Allows searching for a task by name.
