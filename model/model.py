import geopy.distance

from database.DAO import DAO
import networkx as nx


def getPesoTempoPercorrenza(u, v, vel): #metodo statico che non fa parte della classe
    dist=geopy.distance.distance((u.coordX, u.coordY),
                                 (v.coordX, v.coordY)).km #calcola la distanza geodesica (in km) tra due punti, cioè su una sfera
    #riceve due tuple di coordinate geografiche
    time=dist/vel*60 #tempo di percorrenza come distanza tra due fermate / la velocità della linea (lo prendiamo in minuti)
    return time

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo=nx.DiGraph() #grafo semplice ma orientato
        self._idMapFermate={} #dizionario con chiave l'id fermata e valore la fermata stessa
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getShortestPath(self, u, v):
        return nx.single_source_dijkstra(self._grafo, u, v) #implementazione di dijkstra che si aspetta come argomento
        # un grafo, un nodo source e un nodo target
        # e restituisce una tupla con il peso del cammino più breve e la lista di nodi del cammino stesso

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate) #non cambiamo tipo di grafo perché il digraph ammette archi pesati
        #self.addEdgesPesati()
        self.addEdgesPesatiTempi()

    def addEdgesPesatiTempi(self):
        #questo metodo crea degli archi, in cui il peso è pari
        #al tempo di percorrenza di quell'arco, ottenuto come rapporto
        #tra la distanza fra due stazioni e la velocità di percorrenza
        self._grafo.clear_edges()
        allEdgesVel=DAO.getAllEdgesVelocita()
        for e in allEdgesVel:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = getPesoTempoPercorrenza(u, v, e[2]) #e[2] è la velocità
            self._grafo.add_edge(u, v, weight=peso)

    def addEdgesPesati(self):
        #riutilizzo il funzionamento di addedges3
        #ma contando quante volte provo ad aggiungere l'arco
        self._grafo.clear_edges()
        # senza ciclo for, prende le informazioni direttamente dal db
        all_edges = DAO.getAllEdges()
        for conn in all_edges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"]+=1
                #accedo al peso dell'arco e lo incremento (se esiste già)
            else:
                #se non esiste già, lo aggiungo
                self._grafo.add_edge(u, v, weight=1)
                #se la query sql è complicata, conviene questo tipo di approccio
                #in questo caso la query sql sarebbe comunque semplice

    def addEdgesPesatiV2(self):
        #delega il calcolo del peso alla query sql, per semplificarci la vita in python
        self._grafo.clear_edges()
        allEdgesWPeso=DAO.getAllEdgesPesati()
        for e in allEdgesWPeso:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso=e[2]
            self._grafo.add_edge(u, v, weight=peso)

    def getArchiPesoMaggiore(self):
        edges=self._grafo.edges(data=True) #edges è un metodo di grafo
        #il parametro data=True indica che insieme agli archi vengono salvati gli attributi associati
        edgesMaggiori=[]
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1]) ["weight"] > 1: #
                edgesMaggiori.append(e)
        return edgesMaggiori

    def getBFSNodesFromEdges(self, source): #source è il nodo di partenza
        #esplorazione del grafo per livelli(breadth-first)
        archi=nx.bfs_edges(self._grafo, source) #restituisce un iterable di tuple, che rappresentano i nodi visitati
        nodiBFS=[]
        for u, v in archi: #nodo di partenza e di arrivo
            nodiBFS.append(v) #nodo visitato
        return nodiBFS

    def getDFSNodesFromEdges(self, source): #source è il nodo di partenza
        #esplorazione del grafo in profondità(depth-first)
        archi=nx.dfs_edges(self._grafo, source) #restituisce un iterable di tuple, che rappresentano i nodi visitati
        nodiDFS=[]
        for u, v in archi: #nodo di partenza e di arrivo
            nodiDFS.append(v) #nodo visitato
        return nodiDFS

    def getBFSNodesFromTree(self, source):
        tree=nx.bfs_tree(self._grafo, source) #restituisce l'albero di visita
        archi=list(tree.edges())
        nodi=list(tree.nodes())
        return nodi

    def getDFSNodesFromTree(self, source):
        tree=nx.dfs_tree(self._grafo, source) #restituisce l'albero di visita DFS
        archi=list(tree.edges())
        nodi=list(tree.nodes())
        return nodi

    def buildGraph(self): #viene richiamato all'inizio della funzione
        self._grafo.clear() #svuota il grafo ogni volta che viene richiamata la funzione
        self._grafo.add_nodes_from(self._fermate) #perché abbiamo già la lista di fermate prese dal database
        self.add_edges3()

    def add_edges(self):
        self._grafo.clear_edges()
        #prima verifico se i due nodi abbiano una connessione
        for u in self._fermate:
            for v in self._fermate:
                if DAO.has_connection(u,v):
                    self._grafo.add_edge(u,v)
        #TROPPO LENTO: inefficiente per grafi grandi

    def add_edges2(self): #metodo più veloce
        self._grafo.clear_edges()
        #unico ciclo for
        for u in self._fermate:
            for conn in DAO.get_vicini(u):
                v=self._idMapFermate[conn.id_stazA]
                #prendo l'oggetto fermata passando il suo id al dizionario
                self._grafo.add_edge(u,v)

    def add_edges3(self):
        self._grafo.clear_edges()
        #senza ciclo for, prende le informazioni direttamente dal db
        all_edges=DAO.getAllEdges()
        for conn in all_edges:
            u=self._idMapFermate[conn.id_stazP]
            v=self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

    def get_num_nodi(self):
        return len(self._grafo.nodes())

    def get_num_archi(self):
        return len(self._grafo.edges())

    @property
    def fermate(self):
        return self._fermate