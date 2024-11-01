import tkinter as tk
from tkinter import ttk
from base import Database
from task import Task
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Lucas\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Lucas\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

class ToDoApp:
    def __init__(self):
        self.db = Database()
        self.TASK_LIST = list()

        self.NAME = "name"
        self.OUT_YEAR = "year"
        self.OUT_MONTH = "month"
        self.OUT_DAY = "day"

        # started window main
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.geometry("400x400")

        # interface elemnents
        self.setup_ui()

        # execute app
        self.root.mainloop()

    def setup_ui(self):
        # title
        title_label = tk.Label(self.root, text="To-Do List", font=("Arial", 20))
        title_label.pack(pady=10)

        # Frame for inputs and buttons
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # inputs for name and date
        self.name_entry = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.name_entry.grid(row=1, column=0, padx=10)
        self.name_entry.insert(0, self.NAME)

        self.year_entry = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.year_entry.grid(row=2, column=0, padx=10)
        self.year_entry.insert(0, self.OUT_YEAR)

        self.month_entry = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.month_entry.grid(row=3, column=0, padx=10)
        self.month_entry.insert(0, self.OUT_MONTH)

        self.day_entry = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.day_entry.grid(row=4, column=0, padx=10)
        self.day_entry.insert(0, self.OUT_DAY)

        # add task button
        #add_button = tk.Button(input_frame, text="Add Task", font=("Arial", 12), command=self.save_to_db)
        #add_button.grid(row=1, column=1)

        # listbox to show the tasks
        self.task_listbox = tk.Listbox(self.root, height=10, width=60, font=("Arial", 8))
        self.task_listbox.bind('<<ListboxSelect>>', self.click_mouse_and_modify)
        self.task_listbox.pack(pady=10)

        # others button
        self.setup_action_buttons(input_frame)

    #make a funcion to store buttons
    def setup_action_buttons(self, input_frame):
        self.search = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.search.grid(row=5, column=0, padx=10)
        self.search.insert(5, 'Procurar_tarefa')

        tk.Button(input_frame, text="Add Task", font=("Arial", 12), command=self.save_to_db).grid(row=1, column=1)
        tk.Button(input_frame, text='change', font=('Arial', 12), command=self.change).grid(row=5, column=1)
        tk.Button(input_frame, text='delete_task', font=('Arial', 12), command=self.delete_line).grid(row=4, column=1)
        tk.Button(input_frame, text='seach', font=("Arial", 12), command=self.seach).grid(row=2, column=1)
        tk.Button(input_frame, text='update', font=("Arial", 12), command=self.update).grid(row=3, column=1)
        tk.Button(self.root, text="delete_all", font=("Arial", 12), command=self.delete_all).pack(pady=10)

    #store the iformation about mouse click
    def click_mouse(self, event):
        indice_mouse = self.task_listbox.curselection()
        if indice_mouse:
            return self.TASK_LIST[indice_mouse[0]]
        else:
            return None

    #make a function to show the task selected 
    #attributes: self(do be acessible), event(specific the function of the mouse do)
    def click_mouse_and_modify(self, event):
        indice_mouse = self.task_listbox.curselection()
        if indice_mouse:
            task_selected = self.TASK_LIST[indice_mouse[0]]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, task_selected.get_name())
            year, month, day = task_selected.get_data().split('/')
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, year)
            self.month_entry.delete(0, tk.END)
            self.month_entry.insert(0, month)
            self.day_entry.delete(0, tk.END)
            self.day_entry.insert(0, day)
            return task_selected

    def save_to_db(self):
        to_return_task = Task(nome=self.name_entry.get(), data_out=(self.year_entry.get(), self.month_entry.get(), self.day_entry.get()))
        self.db.add_tesk(object_id=to_return_task.get_object_id(), nome=to_return_task.get_name(), data_out=to_return_task.get_data(), iscompleted=False)

    def update(self):
        self.task_listbox.delete(0, tk.END)
        self.TASK_LIST.clear()
        
        task = self.db.recover_task(recover_all=True)
        for num, item in enumerate(task):
            self.TASK_LIST.append(Task(preload=True, preload_tuple=item))
            data_convertida = item[4]
            self.task_listbox.insert(num, f"{item[2]}   {data_convertida}")

    def change(self):
        task_selected = self.click_mouse('<<ListboxSelect>>')
        if task_selected is not None:
            task_modified = Task(
                preload=True,
                preload_tuple=(None, task_selected.get_object_id(), self.name_entry.get(),
                               task_selected.is_completed, f"{self.day_entry.get()}/{self.month_entry.get()}/{self.year_entry.get()}")
            )
            self.db.update_task(id=task_selected.get_object_id(), nome=task_modified.get_name(), data_out=task_modified.get_data(), iscompleted=False)

    def delete_line(self):
        task_selected = self.click_mouse('<<ListboxSelect>>')
        if task_selected:
            dellete_line = task_selected.get_object_id()
            self.db.delete_task(dellete_line)
            self.TASK_LIST.remove(task_selected)
            self.task_listbox.delete(self.task_listbox.curselection())

    def seach(self):
        pesquisa = self.search.get()
        self.task_listbox.delete(0, tk.END)
        base = self.db.search_name(pesquisa)
        for num, item in enumerate(base):
            self.task_listbox.insert(num, f"{item[2]}: {item[4]}")

    def delete_all(self):
        self.db.delete_all()

# Instancia a aplicação
app = ToDoApp()
