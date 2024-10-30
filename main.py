from base import Database
if __name__ == "__main__":
    db = Database()

    db.construir_base()

    db.adicionar_tarefa("tgfdsgfds","tarefa_teste_deletar", True, "11/04/2025")
    db.atualizar_tarefa(1, iscompleted=False)

    db.adicionar_tarefa("dasfssdf", "tarefa 2", False, "11 04 2025")

    temp = db.recuperar_tarefa(recuperar_todas=True)

    




    #verificar = db.recuperar_tarefa(1)

    #db.deletar_tarefa(64)
    #print(verificar)
    #db.deletar_tudo()