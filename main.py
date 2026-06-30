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
    def __init__(self, caminho_banco) -> None:
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

def listar_tarefas(tarefas: list[TarefaDTO]):
    print("*-----------TAREFAS------------*")
    for tarefa in tarefas:
        print(f"{tarefa.id} - {tarefa.titulo} - {'Concluída' if tarefa.concluida else 'Pendente'}")
    print("*------------------------------*")


def selecionar_opcao(repo: TarefaRepository):
    opcao = input(
    """
O que você quer fazer agora?

1. Ver lista de tarefas 
2. Adicionar nova tarefa
3. Concluir tarefa
4. Excluir tarefa
5. Encerrar aplicação
    """)

    match(opcao):
        case "1":
            listar_tarefas(repo.listar())
        case "2":
            nova_tarefa = input("Adicione uma nova tarefa:\n")
            repo.criar(nova_tarefa)
            print("\nTarefa adicionada", end="\n--------")
        case "3":
            tarefa_concluida = input("Insira o número da tarefa concluída:\n")
            repo.concluir(tarefa_concluida)
            print("\nTarefa concluída", end="\n--------")
        case "4":
            tarefa_deletada = input("Insira o número da tarefa a ser excluída:\n")
            repo.deletar(tarefa_deletada)
            print("\nTarefa excluída", end="\n--------")
        case "5":
            exit()
        case "_":
            return "Input inválido. Selecione um número válido."


if __name__ == "__main__":
    tarefa_repository = TarefaRepository(CAMINHO_BANCO)

    while(True):
        selecionar_opcao(tarefa_repository)