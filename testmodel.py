#per fare le prove
from model.model import Model

#istanzio il modello
model=Model()
print("Numero nodi: ", len(model._grafo.nodes))
print("Numero archi: ", model.get_num_archi())

model.buildGraph()

#provo a stampare il n di nodi dopo aver popolato il grafo
print("Numero nodi: ", model.get_num_nodi())
#ottengo lo stesso risultato ma senza accedere alla variabile privata "grafo"
print("Numero archi: ", model.get_num_archi())