#per fare le prove
from model.fermata import Fermata
from model.model import Model

#istanzio il modello
model=Model()
print("Numero nodi: ", len(model._grafo.nodes))
print("Numero archi: ", model.get_num_archi())

model.buildGraphPesato()

#provo a stampare il n di nodi dopo aver popolato il grafo
print("Numero nodi: ", model.get_num_nodi())
#ottengo lo stesso risultato ma senza accedere alla variabile privata "grafo"
print("Numero archi: ", model.get_num_archi())

source=Fermata(2,"Abbesses",2.33855,48.8843)

nodiBFS=model.getBFSNodesFromEdges(source)
print(len(nodiBFS))
for i in range(0, 10):
    print(nodiBFS[i])

nodiBFS2=model.getBFSNodesFromTree(source)
print(len(nodiBFS2))
for i in range(0, 10):
    print(nodiBFS2[i])

nodiDFS=model.getDFSNodesFromEdges(source)
print(len(nodiDFS))
for i in range(0, 10):
    print(nodiDFS[i])

nodiDFS2=model.getDFSNodesFromTree(source)
print(len(nodiDFS2))
for i in range(0, 10):
    print(nodiDFS2[i])

print("=============================================================")

print("Archi con peso 2:")
archiMaggiori=model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a[0], "->", a[1], ":", a[2]["weight"])