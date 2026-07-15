from flask import Flask, jsonify, request
from flask_cors import CORS 
from model import TarefaRepository, TarefaStatus

app = Flask(__name__)
CORS(app)

repo = TarefaRepository()

@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    tarefas_dto = repo.listar()

    # Transforma a lista de DTOs em uma lista de dicionarios
    tarefas_json = [
        {"id": t.id, "titulo": t.titulo, "concluida": t.status.value}
        for t in tarefas_dto
    ]
    return jsonify(tarefas_json)

@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    nova_tarefa = request.json.get("titulo")
    try:
        repo.criar(nova_tarefa)
        return jsonify({"mensagem":"Tarefa criada com sucesso", "titulo": nova_tarefa}), 201
    except Exception as e:
        return jsonify({"error": f"Não foi possível criar a tarefa: {str(e)}"}), 400

@app.route("/tarefas/<int:id_tarefa>", methods=["DELETE"])
def excluir_tarefa(id_tarefa):
    tarefa = repo.get_tarefa(id_tarefa)
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    try:
        repo.deletar(id_tarefa)
        return jsonify({
                "mensagem":"Tarefa excluída com sucesso", 
                "titulo": tarefa.titulo
            })
    except Exception as e:
        return jsonify({"error": f"Não foi possível excluir a tarefa: {str(e)}"}), 400

@app.route("/tarefa/<int:id_tarefa>", methods=["PUT"])
def atualizar_status_tarefa(id_tarefa):
    novo_status = request.json.get("status")
    tarefa = repo.get_tarefa(id_tarefa)

    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    try:
        repo.atualizar(tarefa.id, TarefaStatus[novo_status])
    except Exception as e:
        return jsonify({"error": f"Não foi possível atualizar o estado da tarefa: {str(e)}"}), 400

    return jsonify({"mensagem": "Status atualizado com sucesso"})