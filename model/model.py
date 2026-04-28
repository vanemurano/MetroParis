from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo=nx.DiGraph() #grafo semplice ma orientato
        self._idMapFermate={} #dizionario con chiave l'id fermata e valore la fermata stessa
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def buildGraph(self): #viene richiamato all'inizio della funzione
        self._grafo.clear() #svuota il grafo ogni volta che viene richiamata la funzione
        self._grafo.add_nodes_from(self._fermate) #perché abbiamo già la lista di fermate prese dal database
        self.add_edges3()

    def add_edges(self):
        #prima verifico se i due nodi abbiano una connessione
        for u in self._fermate:
            for v in self._fermate:
                if DAO.has_connection(u,v):
                    self._grafo.add_edge(u,v)
        #TROPPO LENTO

    def add_edges2(self): #metodo più veloce
        #unico ciclo for
        for u in self._fermate:
            for conn in DAO.get_vicini(u):
                v=self._idMapFermate[conn.id_stazA]
                #prendo l'oggetto fermata passando il suo id al dizionario
                self._grafo.add_edge(u,v)

    def add_edges3(self):
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