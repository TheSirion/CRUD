import sqlite3
from pathlib import Path
from dataclasses import dataclass

CAMINHO_BANCO = Path(__file__).resolve().parent / "tarefas.db"

@dataclass
class TarefaDTO:
    id: int
    titulo: str
    concluida: bool

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
                    concluida BOOLEAN NOT NULL DEFAULT 0
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
            conexao.execute("INSERT INTO tarefas (titulo, concluida) VALUES (?, ?)", (titulo, False))

    def concluir(self, id_tarefa) -> None:
        with sqlite3.connect(self.caminho_banco) as conexao:
            conexao.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,))

    def deletar(self, id_tarefa) -> None:
        with sqlite3.connect(self.caminho_banco) as conexao:
            conexao.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))

    def listar(self) -> list[TarefaDTO]:
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tarefas")
            tarefas = cursor.fetchall()
            tarefasDTO = [TarefaDTO(t[0], t[1], bool(t[2])) for t in tarefas]
            return tarefasDTO