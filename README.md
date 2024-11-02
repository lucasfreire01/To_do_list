# 🚨 NEW PROJECT 🚨
# To-Do List Project

## Introduction
The To-Do List project aims to develop a task list using object-oriented programming (OOP) and the Tkinter library for the graphical interface. By creating this application, I seek to enhance my knowledge in OOP and its practical applications, especially in a job market that values these skills.

## Project Structure
The project is divided into three main files:

### 1. `Base.py`
This file manages the database, which contains the following five columns:

- **task_id**: An ID generated based on the count of rows in the database.
- **object_id**: A column with 5 characters used for task selection.
- **name**: The name of the task.
- **is_completed**: An indicator that checks if the task is completed (0 for not completed and 1 for completed).
- **data_out**: The deadline for completing the task.

#### Started Methods
- **fetch_database**: Opens the connection with the database and obtains the cursor.
- **convert_int_to_bool**: Converts the values of 0 or 1 in the `is_completed` column into booleans.
- **convert_bool_to_int**: Performs the inverse transformation for easier manipulation.
- **close_connection**: Closes the connection and the cursor.

#### Functions
- **execute**: Utilizes memory efficiently by opening the connection, executing the task, and closing it afterward.
- **create_base**: Creates the database with the mentioned columns.
- **add_task**: Adds a new task to the database.
- **check_completed**: Checks if the task is completed.
- **recover_task**: Recovers a deleted task.
- **update_task**: Allows the user to modify an existing task.
- **delete_task**: Removes a specific task.
- **delete_all**: Deletes all tasks in the database.
- **search_task**: Allows searching for a task by name.

### 2. `GUI.py`
This file is responsible for the graphical interface of the application. Using the Tkinter library, it creates an intuitive interface that allows users to interact easily with the task list. The main functionalities of the GUI include:

- **Input Forms**: Fields to add new tasks, with validation to ensure necessary information is filled.
- **Task List**: Displays all tasks stored in the database, allowing users to quickly view their pending activities.
- **Action Buttons**: Buttons for adding, updating, deleting, and searching tasks, making user interaction with the application seamless.
- **Task Status**: Visually indicates which tasks are completed, allowing for effective time and responsibility management.

### 3. `Task.py`
This file contains the `Task` class, which defines the data model for tasks. The class includes relevant attributes and methods, such as:

- **Attributes**:
  - `task_id`: Unique ID of the task.
  - `name`: Name of the task.
  - `is_completed`: Status of the task completion.
  - `data_out`: Deadline for the task.

- **Methods**:
  - `mark_as_completed()`: Marks the task as completed.
  - `update_name(new_name)`: Updates the name of the task.
  - `set_deadline(deadline)`: Sets a new deadline for the task.

## Interaction Between Components
The interaction between the `Base`, `Task`, and `GUI` components is essential for the functionality of the To-Do List application:

1. **Task Creation and Management**:
   - When a user adds a new task through the `GUI`, the input is processed and used to create a new `Task` object. This object contains all the necessary details, such as the task name and deadline.
   - The `GUI` calls the `add_task` function from `Base` to store the task details in the database. This function handles the database operations, ensuring the task is saved correctly.

2. **Displaying Tasks**:
   - The `GUI` fetches all tasks from the database by invoking the `fetch_database` method in `Base`. This method retrieves the current task list and returns it to the GUI for display.
   - The tasks are shown in a list format, with their completion status visually indicated. Users can see which tasks are pending and which are completed.

3. **Updating Tasks**:
   - If a user decides to update a task, the `GUI` collects the modified information and creates an updated `Task` object.
   - The `update_task` function in `Base` is then called, which updates the task information in the database.

4. **Deleting Tasks**:
   - Users can delete a task directly from the GUI. Upon confirmation, the GUI calls the `delete_task` function in `Base`, which removes the selected task from the database.
   - Additionally, users can delete all tasks using the `delete_all` function.

5. **Task Completion**:
   - The GUI allows users to mark tasks as completed. When this action is taken, the corresponding `Task` object's `mark_as_completed` method is invoked, and the `update_task` function in `Base` is called to reflect this change in the database.

## Application Features
- **Add Tasks**: Users can enter new tasks with a name and a deadline, which are saved in the database.
- **Update Tasks**: The application allows users to edit details of existing tasks.
- **Delete Tasks**: Users can remove individual tasks or delete all tasks at once.
- **Search Tasks**: The application enables searching for specific tasks by name.
- **Status Visualization**: Completed tasks are highlighted, providing a clear view of user progress.

## Conclusion
The To-Do List application is a practical and efficient solution for managing daily tasks, helping users stay organized and productive. The implementation of the SQLite database ensures that task information is saved permanently, providing a continuous and effective user experience.
