import tkinter as tk
from tkinter import ttk
from base import Database
from tarefa import Tarefa
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Lucas\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Lucas\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

class ToDoApp:
    def __init__(self):
        self.db = Database()
        self.TAREFAS_LIST = list()

        self.NOME = "Insira nome"
        self.VENC_YEAR = "Insira ano"
        self.VENC_MONTH = "Insira mês"
        self.VENC_DAY = "Insira dia"

        # Inicialização da janela principal
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.geometry("400x400")

        # Elementos de interface
        self.setup_ui()

        # Executa a aplicação
        self.root.mainloop()

    def setup_ui(self):
        # Título
        title_label = tk.Label(self.root, text="To-Do List", font=("Arial", 20))
        title_label.pack(pady=10)

        # Frame para entradas e botões
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        # Entradas para nome e data
        self.name_entry = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.name_entry.grid(row=1, column=0, padx=10)
        self.name_entry.insert(0, self.NOME)

        self.ano_inserido = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.ano_inserido.grid(row=2, column=0, padx=10)
        self.ano_inserido.insert(0, self.VENC_YEAR)

        self.mes_inserido = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.mes_inserido.grid(row=3, column=0, padx=10)
        self.mes_inserido.insert(0, self.VENC_MONTH)

        self.dia_inserido = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.dia_inserido.grid(row=4, column=0, padx=10)
        self.dia_inserido.insert(0, self.VENC_DAY)

        # Botão para adicionar tarefa
        add_button = tk.Button(input_frame, text="Add Task", font=("Arial", 12), command=self.save_to_db)
        add_button.grid(row=1, column=1)

        # Listbox para exibir tarefas
        self.task_listbox = tk.Listbox(self.root, height=10, width=60, font=("Arial", 8))
        self.task_listbox.bind('<<ListboxSelect>>', self.click_mouse_and_modify)
        self.task_listbox.pack(pady=10)

        # Botões de ações adicionais
        self.setup_action_buttons(input_frame)

    def setup_action_buttons(self, input_frame):
        self.procurar_campo = tk.Entry(input_frame, width=25, font=("Arial", 14), fg='grey')
        self.procurar_campo.grid(row=5, column=0, padx=10)
        self.procurar_campo.insert(5, 'Procurar_tarefa')

        tk.Button(input_frame, text='modificar', font=('Arial', 12), command=self.modificar).grid(row=5, column=1)
        tk.Button(input_frame, text='deletar linha', font=('Arial', 12), command=self.deletar_tarefa).grid(row=4, column=1)
        tk.Button(input_frame, text='Procurar', font=("Arial", 12), command=self.procurar).grid(row=2, column=1)
        tk.Button(input_frame, text='Atualizar', font=("Arial", 12), command=self.atualizar).grid(row=3, column=1)
        tk.Button(self.root, text="Deletar Tudo", font=("Arial", 12), command=self.deletar_tudo).pack(pady=10)

    def click_mouse(self, evento):
        indice_mouse = self.task_listbox.curselection()
        if indice_mouse:
            return self.TAREFAS_LIST[indice_mouse[0]]
        else:
            return None

    def click_mouse_and_modify(self, evento):
        indice_mouse = self.task_listbox.curselection()
        if indice_mouse:
            tarefa_selecionada = self.TAREFAS_LIST[indice_mouse[0]]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, tarefa_selecionada.get_name())
            ano, mes, dia = tarefa_selecionada.get_data().split('/')
            self.ano_inserido.delete(0, tk.END)
            self.ano_inserido.insert(0, ano)
            self.mes_inserido.delete(0, tk.END)
            self.mes_inserido.insert(0, mes)
            self.dia_inserido.delete(0, tk.END)
            self.dia_inserido.insert(0, dia)
            return tarefa_selecionada

    def carregar_dados(self):
        tarefas_tudo = self.db.carregar_tudo(Tarefa)
        for tarefa in tarefas_tudo:
            self.task_listbox.insert(tk.END, f"{Tarefa['nome']} - {Tarefa['data_vencimento']}")

    def save_to_db(self):
        to_return_tarefa = Tarefa(nome=self.name_entry.get(), data_vencimento=(self.ano_inserido.get(), self.mes_inserido.get(), self.dia_inserido.get()))
        self.db.adicionar_tarefa(object_id=to_return_tarefa.get_object_id(), nome=to_return_tarefa.get_name(), data_vencimento=to_return_tarefa.get_data(), iscompleted=False)

    def atualizar(self):
        self.task_listbox.delete(0, tk.END)
        self.TAREFAS_LIST.clear()
        
        tarefas = self.db.recuperar_tarefa(recuperar_todas=True)
        for num, item in enumerate(tarefas):
            self.TAREFAS_LIST.append(Tarefa(preload=True, preload_tuple=item))
            data_convertida = item[4]
            self.task_listbox.insert(num, f"{item[2]}   {data_convertida}")

    def modificar(self):
        tarefa_selecionada = self.click_mouse('<<ListboxSelect>>')
        if tarefa_selecionada is not None:
            tarefa_modificada = Tarefa(
                preload=True,
                preload_tuple=(None, tarefa_selecionada.get_object_id(), self.name_entry.get(),
                               tarefa_selecionada.is_completed, f"{self.dia_inserido.get()}/{self.mes_inserido.get()}/{self.ano_inserido.get()}")
            )
            self.db.atualizar_tarefa(id=tarefa_selecionada.get_object_id(), nome=tarefa_modificada.get_name(), data_vencimento=tarefa_modificada.get_data(), iscompleted=False)

    def deletar_tarefa(self):
        tarefa_selecionada = self.click_mouse('<<ListboxSelect>>')
        if tarefa_selecionada:
            deletar_linha = tarefa_selecionada.get_object_id()
            self.db.deletar_tarefa(deletar_linha)
            self.TAREFAS_LIST.remove(tarefa_selecionada)
            self.task_listbox.delete(self.task_listbox.curselection())

    def procurar(self):
        pesquisa = self.procurar_campo.get()
        self.task_listbox.delete(0, tk.END)
        base = self.db.pesquisar_nome(pesquisa)
        for num, item in enumerate(base):
            self.task_listbox.insert(num, f"{item[2]}: {item[4]}")

    def deletar_tudo(self):
        self.db.deletar_tudo()

# Instancia a aplicação
app = ToDoApp()
