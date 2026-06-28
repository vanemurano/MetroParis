import copy

import geopy.distance

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph=nx.DiGraph() # semplice, orientato e pesato
        self._nodes=[]
        self._bestPath=[]
        self._bestScore=0

    def buildGraph(self):
        self._nodes=DAO.getAllNodes()
        self._graph.add_nodes_from(self._nodes)
        for c1, c2 in DAO.getAllEdges():
            if c1 in self._nodes and c2 in self._nodes:
                peso=DAO.getEdgeWeight(c1, c2)
                self._graph.add_edge(c1, c2, weight=peso)

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)

    def getMinMaxWeight(self):
        maxEdge=max(self._graph.edges(data="weight"), key=lambda x: x[2])
        minEdge=min(self._graph.edges(data="weight"), key=lambda x: x[2])
        return float(minEdge[2]), float(maxEdge[2]) # pesi dell'arco minimo e massimo

    def contaArchi(self, s: float):
        numMaggiori=0
        numMinori=0
        for c1, c2, peso in self._graph.edges(data="weight"):
            if peso<s:
                numMinori+=1
            if peso>s:
                numMaggiori+=1
        return numMinori, numMaggiori

    def getBestPath(self, soglia):
        parziale=[]
        self._bestPath=[]
        self._bestScore=-10000 # impossibile da raggiungere
        for n in self._nodes:
            parziale.append(n)
            self._ricorsione(soglia, parziale, 0)
            parziale.pop()
        return self._bestPath, self._bestScore

    def _ricorsione(self, s, parziale, score):
        # condizione di ottimalità
        if score>self._bestScore:
            self._bestPath=copy.deepcopy(parziale)
            self._bestScore=score
        for n in self._graph.successors(parziale[-1]):
            peso_arco=self._graph[parziale[-1]][n]["weight"]
            if peso_arco>s and n not in parziale:
                parziale.append(n)
                nuovo_score=score+peso_arco
                self._ricorsione(s, parziale, nuovo_score)
                parziale.pop() # backtracking

