from model import TarefaRepository
from view import TarefaView
from controller import TarefaController

if __name__ == "__main__":
    model = TarefaRepository()
    view = TarefaView()
    controller = TarefaController(model, view)

    view.mainloop()