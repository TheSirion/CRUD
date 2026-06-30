import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "tarefas.db"

def inicializar_banco():
    # conexao, cursor = abrir_conexao()
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
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

def criar_tarefa(titulo):
    # conexao, cursor = abrir_conexao()
    # ? é usado para evitar SQL injection
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("INSERT INTO tarefas (titulo, concluida) VALUES (?, ?)", (titulo, False))

def concluir_tarefa(id_tarefa):
    # conexao, cursor = abrir_conexao()
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,))

def deletar_tarefa(id_tarefa):
    # conexao, cursor = abrir_conexao()
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))

def mostrar_tarefas():
    # conexao, cursor = abrir_conexao()
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()
    
    for tarefa in tarefas:
        print(f"{tarefa[0]} - {tarefa[1]} - {'Concluída' if tarefa[2] else 'Pendente'}")

def selecionar_opcao():
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
            mostrar_tarefas()
        case "2":
            nova_tarefa = input("Adicione uma nova tarefa:\n")
            criar_tarefa(nova_tarefa)
            print("\nTarefa adicionada")
        case "3":
            tarefa_concluida = input("Insira o número da tarefa concluída:\n")
            concluir_tarefa(tarefa_concluida)
            print("\nTarefa concluída")
        case "4":
            tarefa_deletada = input("Insira o número da tarefa a ser excluída:\n")
            deletar_tarefa(tarefa_deletada)
            print("\nTarefa excluída")
        case "5":
            exit()
        case "_":
            print("Input inválido. Selecione um número válido.")


if __name__ == "__main__":
    inicializar_banco()
    mostrar_tarefas()

    while(True):
        selecionar_opcao()