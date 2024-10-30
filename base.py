import random
from datetime import datetime
import sqlite3
import tarefa

HARD_CODED_DB = "./tarefas.db"


class Database:

    def __init__(self, DB=None):

        self.db = HARD_CODED_DB

        
        if DB is not None:
            self.db = DB

        self.construir_base()

    @staticmethod
    def fetch_database(dir):
        conexao = sqlite3.connect(dir)
        cursor = conexao.cursor()
        return conexao, cursor


    @staticmethod
    def convert_int_to_bool(integer):
        return False if integer == 0 else True

    @staticmethod
    def convert_bool_to_int(bool):
        return 1 if bool else 0

    @staticmethod
    def fechar_conexao(conexao, cursor):
        cursor.close()
        conexao.close()

    def execute(self, query, params=True,returnable=False, args=()):

        # ABRIR CONEXAO
        conexao, cursor = self.fetch_database(self.db)

        # EXECUTAR QUERY

        if params:
            cursor.execute(query, args)

        else:
            cursor.execute(query)

        # commit
        conexao.commit()

        # TEM QUE RETORNAR ALGUM VALOR?
      

        if returnable:
            temp = cursor.fetchall()
            print(temp)
            self.fechar_conexao(*(conexao, cursor))
            return temp

        self.fechar_conexao(*(conexao, cursor))
        # FECHAR CONEXÃO

    def construir_base(self):

        self.execute(
            """CREATE TABLE IF NOT EXISTS tarefa(
                       tarefa_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       object_id INTEGER NOT NULL,
                       nome VARCHAR(100) NOT NULL,
                       iscompleted INTEGER NOT NULL CHECK(iscompleted IN (0, 1)),
                       data_vencimento TEXT NOT NULL)
                       """,
            params=False,
        )

        # Verificar ou criar uma forma de abrir e fechar o cursor em cada chamada (NÃO MANTER ABERTO.)
        # self.cursor.close()

    def adicionar_tarefa(self, object_id: str, nome: str, data_vencimento: str, iscompleted: bool
                         ):

        # DATE FORMAT: "11/04/2025"
        completed_status = self.convert_bool_to_int(iscompleted)

        #data_formatada = self.converter_data(data_vencimento).strftime("%d/%m/%Y")
        

        self.execute(
            """INSERT INTO tarefa (object_id, nome, iscompleted, data_vencimento)
        values(?,?,?,?)""",
            args=(object_id, nome, completed_status, data_vencimento),
        )

        print(f"ADDED TO DB {(object_id, nome, completed_status, data_vencimento)}")

    def verificar_completo(self, tarefa: str):
        self.cursor.execute(
            """
        UPDATE tarefa SET iscompleted = 1 WHERE object_id = ?""",
            args=(tarefa,),
        )

    
    def recuperar_tarefa(self, id=None, recuperar_todas=False) -> tuple:

        if recuperar_todas:
            tarefas = self.execute(
            """SELECT * FROM tarefa""", returnable=True
        )
            
            # LOGICA PARA APLICCAR TRANSFORMAÇÃO PARA TODAS AS TAREFAS RETORNADAS

            for index, tarefa in enumerate(tarefas):
    
                #data_convertida = self.converter_data(tarefa[4]).strftime("%d/%m/%Y")
                print(tarefa)
                tarefas[index] = (

                tarefa[0],
                tarefa[1],
                tarefa[2],
                self.convert_int_to_bool(tarefa[3]),
                tarefa[4],

                )

            # --------------------------------
            return tarefas
            
        elif id is not None and recuperar_todas == False: 

            tarefa = self.execute(
                """SELECT * FROM tarefa WHERE object_id = ?""", returnable=True,args=(id,)
            )
            # transformando em tupla
            # recuperar a data de vencimento em datetime
           # data_convertida = self.converter_data(tarefa[4]).strftime("%d/%m/%Y")

            return (
                tarefa[0],
                tarefa[1],
                tarefa[2],
                self.convert_int_to_bool(tarefa[3]),
                tarefa[4],
            )

    def atualizar_tarefa(
        self, id: str, nome=None, iscompleted=None, data_vencimento=None
    ):

        # Nome e data de vencimento está em None para ser opicional a busca com esses atributos
        if nome is not None:
            self.execute(
                """UPDATE tarefa SET nome = ? WHERE object_id = ?""", args=(nome, id)
            )

        # Verificando se o usuario passou o valor correto e atualisando ele.
        if iscompleted is not None:
            self.execute(
                """UPDATE tarefa SET iscompleted = ? WHERE object_id = ?""",
                args=(self.convert_bool_to_int(iscompleted), id),
            )

        if data_vencimento is not None:
            self.execute(
                """UPDATE tarefa SET data_vencimento = ? WHERE object_id = ?""",
                args=(data_vencimento, id),
            )

    def deletar_tarefa(self, id: str):
        self.execute("""DELETE FROM tarefa WHERE object_id = ?""", args=(id,))

    def deletar_tudo(self):
        self.execute("""DELETE FROM tarefa """)

    def pesquisar_nome(self, nome:str):
        dados = self.execute("""SELECT * FROM tarefa WHERE nome LIKE ?""", args=(f"%{nome}%",), returnable=True)
        return dados






