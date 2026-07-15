import tkinter as tk

class TarefaView(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("400x400")

        # o controlador começa vazio e será injetado depois
        self.controller = None

        # método que vai desenhar nossos componentes
        self._configurar_tela()

    def set_controller(self, controller):
        """Método para o main.py injetar o controlador no view"""
        self.controller = controller

    def _configurar_tela(self):
        self.entrada_titulo = tk.Entry()