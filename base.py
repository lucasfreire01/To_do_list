import random
from datetime import datetime
import sqlite3
import task
import os

HARD_CODED_DB = "./tasks.db"

os.environ['TCL_LIBRARY'] = r'C:\Users\Lucas\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Lucas\AppData\Local\Programs\Python\Python313\tcl\tk8.6'
class Database:

    def __init__(self, DB=None):

        self.db = HARD_CODED_DB

        
        if DB is not None:
            self.db = DB

        self.create_base()

    #started the connection
    @staticmethod
    def fetch_database(dir):
        connect = sqlite3.connect(dir)
        cursor = connect.cursor()
        return connect, cursor

    @staticmethod
    def convert_int_to_bool(integer):
        return False if integer == 0 else True

    @staticmethod
    def convert_bool_to_int(bool):
        return 1 if bool else 0

    @staticmethod
    def close_connection(connect, cursor):
        cursor.close()
        connect.close()

    #create a execute to open make the method and close to imporve the memory use 
    def execute(self, query, params=True,returnable=False, args=()):

        # open connect
        connect, cursor = self.fetch_database(self.db)

        # execute the query

        if params:
            cursor.execute(query, args)

        else:
            cursor.execute(query)

        # commit
        connect.commit()

        # if have value
      

        if returnable:
            temp = cursor.fetchall()
            print(temp)
            self.close_connection(*(connect, cursor))
            return temp

        self.close_connection(*(connect, cursor))
        # close connection

    def create_base(self):

        self.execute(
            """CREATE TABLE IF NOT EXISTS task(
                       task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       object_id INTEGER NOT NULL,
                       name VARCHAR(100) NOT NULL,
                       iscompleted INTEGER NOT NULL CHECK(iscompleted IN (0, 1)),
                       data_out TEXT NOT NULL)
                       """,
            params=False,
        )

    def add_tesk(self, object_id: str, name: str, data_out: str, iscompleted: bool
                         ):

        # DATE FORMAT: "11/04/2025"
        completed_status = self.convert_bool_to_int(iscompleted)
        

        #execute the query with paramns
        self.execute(
            """INSERT INTO task (object_id, name, iscompleted, data_out)
        values(?,?,?,?)""",
            args=(object_id, name, completed_status, data_out),
        )

        print(f"ADDED TO DB {(object_id, name, completed_status, data_out)}")

    def check_completed(self, task: str):
        self.cursor.execute(
            """
        UPDATE task SET iscompleted = 1 WHERE object_id = ?""",
            args=(task,),
        )

    
    def recover_task(self, id=None, recover_all=False) -> tuple:

        #if the use need recover all task
        if recover_all:
            tasks = self.execute(
            """SELECT * FROM task""", returnable=True
        )

            #print in the app the task's recover
            for index, task in enumerate(tasks):
    
                print(task)
                tasks[index] = (

                task[0],
                task[1],
                task[2],
                self.convert_int_to_bool(task[3]),
                task[4],

                )

            # --------------------------------
            return tasks
            
        #made a query with a specific id
        elif id is not None and recover_all == False: 

            task = self.execute(
                """SELECT * FROM task WHERE object_id = ?""", returnable=True,args=(id,)
            )
            #print the result
            return (
                task[0],
                task[1],
                task[2],
                self.convert_int_to_bool(task[3]),
                task[4],
            )

    def update_task(
        self, id: str, name=None, iscompleted=None, data_out=None
    ):

        # name and data_out is None to be opcional
        if name is not None:
            self.execute(
                """UPDATE task SET name = ? WHERE object_id = ?""", args=(name, id)
            )

        # checking if user pasted the right values
        if iscompleted is not None:
            self.execute(
                """UPDATE task SET iscompleted = ? WHERE object_id = ?""",
                args=(self.convert_bool_to_int(iscompleted), id),
            )

        if data_out is not None:
            self.execute(
                """UPDATE task SET data_out = ? WHERE object_id = ?""",
                args=(data_out, id),
            )

    def delete_task(self, id: str):
        self.execute("""DELETE FROM task WHERE object_id = ?""", args=(id,))

    def delete_all(self):
        self.execute("""DELETE FROM task """)

    def search_name(self, name:str):
        data = self.execute("""SELECT * FROM task WHERE name LIKE ?""", args=(f"%{name}%",), returnable=True)
        return data
    
app = Database()






