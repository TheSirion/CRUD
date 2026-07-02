class TarefaController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Vinculamos o controller à view
        self.view.set_controller(self)
        self.atualizar_tela()

    def atualizar_tela(self):
        tarefas = self.model.listar()
        self.view.atualizar_lista(tarefas)

    def adicionar_tarefa(self, titulo):
        self.model.criar(titulo)
        self.atualizar_tela()

    def concluir_tarefa(self, id_tarefa):
        self.model.concluir(id_tarefa)
        self.atualizar_tela()

    def deletar_tarefa(self, id_tarefa):
        self.model.get_id = id_tarefa
        self.model.deletar(id_tarefa)
        self.atualizar_tela()