import sqlite3
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

CAMINHO_BANCO = Path(__file__).resolve().parent / "tarefas.db"

class TarefaStatus(Enum):
    PENDING = "A FAZER"
    IN_PROGRESS = "EM PROGRESSO"
    COMPLETED = "CONCLUÍDO"

@dataclass
class TarefaDTO:
    id: int
    titulo: str
    status: TarefaStatus

class TarefaRepository:
    def __init__(self, caminho_banco = CAMINHO_BANCO) -> None:
        self.caminho_banco = caminho_banco
        self._inicializar_banco()


    def _inicializar_banco(self) -> None:
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()

            sql_criar_tabela = """
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    concluida TEXT NOT NULL DEFAULT 'PENDING'
                );
            """

            # executa o SQL
            cursor.execute(sql_criar_tabela)
        
        # Confirma a alteração e fecha a conexão
        # conexao.commit()
        # conexao.close()

    def criar(self, titulo) -> None:
        # ? é usado para evitar SQL injection
        with sqlite3.connect(self.caminho_banco) as conexao:
            conexao.execute("INSERT INTO tarefas (titulo, concluida) VALUES (?, ?)", (titulo, TarefaStatus.PENDING.name))

    def atualizar(self, id_tarefa, novo_status: TarefaStatus) -> None:
        with sqlite3.connect(self.caminho_banco) as conexao:
            conexao.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (novo_status.name, id_tarefa,))

    def deletar(self, id_tarefa) -> None:
        with sqlite3.connect(self.caminho_banco) as conexao:
            conexao.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))

    def get_tarefa(self, id_tarefa) -> TarefaDTO:
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id_tarefa,))
            tarefa = cursor.fetchone()

            if tarefa:
                return TarefaDTO(tarefa[0], tarefa[1], TarefaStatus[tarefa[2]])
            return None

    def listar(self) -> list[TarefaDTO]:
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tarefas")
            tarefas = cursor.fetchall()
            return [TarefaDTO(t[0], t[1], TarefaStatus[t[2]]) for t in tarefas]
