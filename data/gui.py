import tkinter as tk
from tkinter import ttk
from base import Database
from tarefa import Tarefa

db = Database()

TAREFAS_LIST = list()


NOME = "Insira nome"

VENC_YEAR = "Insira ano"
VENC_MONTH = "Insira mês"
VENC_DAY = "Insira dia"

def click_mouse(evento):

    # SELECIONA DO LISTBOX
    indice_mouse = task_listbox.curselection()
        
    if indice_mouse:
        return TAREFAS_LIST[indice_mouse[0]]
    else:
         return None
    
def click_mouse_and_modify(evento):

        indice_mouse = task_listbox.curselection()

        if indice_mouse != ():

            print(indice_mouse)
            tarefa_selecionada = TAREFAS_LIST[indice_mouse[0]]

            name_entry.delete(0, tk.END)
            name_entry.insert(0, tarefa_selecionada.get_name())

            ano, mes , dia = tarefa_selecionada.get_data().split('/')

            ano_inserido.delete(0, tk.END)
            ano_inserido.insert(0, ano)
            
            mes_inserido.delete(0, tk.END)
            mes_inserido.insert(0, mes)

            dia_inserido.delete(0, tk.END)
            dia_inserido.insert(0, dia)

            return tarefa_selecionada


# Create the main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

# Title label
title_label = tk.Label(root, text="To-Do List", font=("Arial", 20))
title_label.pack(pady=10)

# Frame for entry box and add button
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Entry box to insert the name
name_entry = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
name_entry.grid(row=1, column=0, padx=10)
name_entry.insert(0, NOME)

# Entry box to insert the due date
ano_inserido = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
ano_inserido.grid(row=2, column=0, padx=10)
ano_inserido.insert(0, VENC_YEAR)

mes_inserido = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
mes_inserido.grid(row=3, column=0, padx=10)
mes_inserido.insert(0, VENC_MONTH)

dia_inserido = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
dia_inserido.grid(row=4, column=0, padx=10)
dia_inserido.insert(0, VENC_DAY)

#Juntando a data da maneira desejada



def carregar_dados():
    tarefas_tudo = db.carregar_tudo(Tarefa)
    for tarefa in tarefas_tudo:
        task_listbox.insert(tk.END, f"{Tarefa['nome']} - {Tarefa['data_vencimento']}")

def save_to_db():
    to_return_tarefa = Tarefa(nome = name_entry.get(), data_vencimento= (ano_inserido.get(), mes_inserido.get(), dia_inserido.get()) )
    db.adicionar_tarefa(object_id=to_return_tarefa.get_object_id(), 
                        nome=to_return_tarefa.get_name(), 
                        data_vencimento=to_return_tarefa.get_data(),
                        iscompleted=False
    )

# Button to add a new task
add_button = tk.Button(input_frame, text="Add Task", font=("Arial", 12), command=save_to_db)
add_button.grid(row=1, column=1)


task_listbox = tk.Listbox(root, height=10, width=60, font=("Arial", 8))

object_id = []

def atualizar():
      tarefas = db.recuperar_tarefa(recuperar_todas=True)
      for num, item in enumerate(tarefas):
        TAREFAS_LIST.append(Tarefa(preload=True, preload_tuple=item))  
        data_convertida = item[4]
        task_listbox.insert(num, f" {item[2]}   {data_convertida}")


procurar_campo = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
procurar_campo.grid(row=5, column=0, padx=10)
procurar_campo.insert(5, 'Procurar_tarefa')



def modificar():

    # PEGAR TAREFA PARA MODIFICAR (CLICK MOUSE)
        tarefa_selecionada = click_mouse('<<ListboxSelect>>')
 
        if tarefa_selecionada is not None:
            tarefa_modificada = Tarefa(
                 preload=True, 
                 preload_tuple=(None, 
                 tarefa_selecionada.get_object_id(),
                 name_entry.get(),
                 tarefa_selecionada.is_completed,
                 f"{dia_inserido.get()}/{mes_inserido.get()}/ {ano_inserido.get()}"
                 )
            )

        else:
             print('Nenhuma tarefa selecionada')
            


        db.atualizar_tarefa(id=tarefa_selecionada.get_object_id(), 
                        nome=tarefa_modificada.get_name(), 
                        data_vencimento=tarefa_modificada.get_data(),
                        iscompleted=False
                        )
    

    # PEGAR ATRIBUTO MODIFIADO


    # RODAR ATUALIZAR TAREFA -> ARGUMENTO MODIFICADO PELO USUARIO


def deletar_tarefa():
    tarefa_selecionada = click_mouse('<<ListboxSelect>>')
    if tarefa_selecionada:
        deletar_linha = tarefa_selecionada.get_object_id()
        db.deletar_tarefa(deletar_linha)

        TAREFAS_LIST.remove(tarefa_selecionada)

        task_listbox.delete(task_listbox.curselection())

def procurar():

    pesquisa = procurar_campo.get()
    task_listbox.delete(0, tk.END)
    base = db.pesquisar_nome(pesquisa)
    for num, item in enumerate(base):
        task_listbox.insert(num, f"{item[2]}: {item[4]}")


task_listbox.bind('<<ListboxSelect>>', click_mouse_and_modify)

botão_modificar = tk.Button(input_frame, text='modificar', font=('Arial', 12), command=modificar)
botão_modificar.grid(row=5, column=1)

botão_excluir = tk.Button(input_frame, text='deletar linha', font=('Arial', 12), command=deletar_tarefa)
botão_excluir.grid(row=4, column=1)


botão_procurar = tk.Button(input_frame, text='Procurar', font=("Arial", 12), command=procurar)
botão_procurar.grid(row=2, column=1)

atualizar_botão = tk.Button(input_frame, text='Atualizar', font=("Arial", 12), command=atualizar)
atualizar_botão.grid(row=3, column=1)

def deletar_tudo():
    terefa = db.deletar_tudo()

# Listbox to display tasks






task_listbox.pack(pady=10)

# Frame for action buttons
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

# Button to remove a selected task

# Button to clear all tasks      
clear_button = tk.Button(action_frame, text="Deletar Tudo", font=("Arial", 12), command=deletar_tudo)
clear_button.grid(row=0, column=1, padx=10)

# Run the application
root.mainloop()
