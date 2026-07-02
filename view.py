import tkinter as tk
from tkinter import messagebox

class TarefaView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de tarefas - MVC")
        self.geometry("450x400")
        self.controller = None
        self._construir_interface()

    def _construir_interface(self):
        # Campo de Entrada
        self.entrada_titulo = tk.Entry(self, font=("Arial", 12), width=30)
        self.entrada_titulo.pack(pady=10)

        # Botão Adicionar
        btn_adicionar = tk.Button(self, text="Adicionar Tarefa", command=self._on_adicionar)
        btn_adicionar.pack(pady=5)

        # Lista de Tarefas (Listbox)
        self.lista_visual = tk.Listbox(self, font=("Arial", 11), width=45, height=12)
        self.lista_visual.pack(pady=10)

        # Botões de Ação embaixo da lista
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=5)

        btn_concluir = tk.Button(frame_botoes, text="Concluir Selecionada", command=self._on_concluir)
        btn_concluir.pack(side=tk.LEFT, padx=5)

        btn_deletar = tk.Button(frame_botoes, text="Excluir Selecionada", command=self._on_deletar)
        btn_deletar.pack(side=tk.LEFT, padx=5)

    def set_controller(self, controller):
        self.controller = controller

    def atualizar_lista(self, tarefas):
        """Preenche o Listbox com os DTOs recebidos do Controller"""
        self.lista_visual.delete(0, tk.END)
        # Guardamos os objetos originais mapeados pelo índice visual do Listbox
        self.tarefas_na_tela = tarefas 
        
        for tarefa in tarefas:
            status = "🟢 Concluída" if tarefa.concluida else "🟡 Pendente"
            self.lista_visual.insert(tk.END, f"{tarefa.id} | {tarefa.titulo} [{status}]")

    def _get_tarefa_selecionada(self):
        try:
            index = self.lista_visual.curselection()[0]
            return self.tarefas_na_tela[index]
        except IndexError:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa na lista.")
            return None

    # Gatilhos de Eventos que repassam a ordem para o Controller
    def _on_adicionar(self):
        titulo = self.entrada_titulo.get().strip()
        if titulo:
            self.controller.adicionar_tarefa(titulo)
            self.entrada_titulo.delete(0, tk.END)
        else:
            messagebox.showwarning("Erro", "O título não pode ser vazio.")

    def _on_concluir(self):
        tarefa = self._get_tarefa_selecionada()
        if tarefa:
            self.controller.concluir_tarefa(tarefa.id)

    def _on_deletar(self):
        tarefa = self._get_tarefa_selecionada()
        if tarefa:
            self.controller.deletar_tarefa(tarefa.id)
    