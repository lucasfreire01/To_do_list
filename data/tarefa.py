import tkinter as tk
from tkinter import messagebox
import sqlite3
import random as rd
import datetime
import string


con = sqlite3.connect("base.db")


#Alocando tarefa atual

class Tarefa:

    # Constructor -> construindo o objecto

    # Recebe argumentos. 
    def __init__(self, nome=None, data_vencimento=None, is_completed=False, preload=False, preload_tuple=None):
        
       
        if not preload:
            data_vencimento_str = f'{data_vencimento[2]}/{data_vencimento[1]}/{data_vencimento[0]}'
            self.data = data_vencimento_str
            self.nome = nome  
            self.is_completed = is_completed
            self.object_id = self.gerar_id()

        else:

            # (47, '0el\np', 'teste1', 0, '31/11/2024')

            self.data = preload_tuple[4]
            self.nome = preload_tuple[2]  
            self.is_completed = preload_tuple[3]  
            self.object_id = preload_tuple[1]  


    
    @staticmethod
    def gerar_id(n=5):
        printable = string.printable
        return "".join([printable[rd.choice(range(0, len(printable)))] for _ in range(n)])

    @staticmethod
    def converter_data(data: str) -> str:
        data_formatada = datetime.datetime.strptime(data, "%Y-%m-%d")
        return data_formatada.strftime("%d/%m/%Y")
    
    
    #Usando getters para encapsular atributos privados
    def get_name(self):
        return self.nome
    
    def get_data(self):
        return self.data
    
    def get_object_id(self):
        return self.object_id
