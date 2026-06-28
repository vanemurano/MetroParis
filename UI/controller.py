import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self):
        self._model.buildGraph()
        self._pesoMin=round(self._model.getMinMaxWeight()[0], 6)
        self._pesoMax=round(self._model.getMinMaxWeight()[1], 6)
        self._view.lst_result.controls.append(
            ft.Text(f"Grafo creato: {self._model.getNNodes()} nodi e {self._model.getNEdges()} archi\n"
                    f"Peso minimo = {self._pesoMin}, peso massimo = {self._pesoMax}")
        )
        self._view.update_page()

    def handleContaArchi(self, e):
        soglia=self._view._txtInN.value
        if soglia=="":
            self._view.lst_result.controls.append(
                ft.Text(f"Inserire valore soglia!", color="red")
            )
            self._view.update_page()
            return
        try:
            floatS=float(soglia)
        except ValueError:
            self._view.lst_result.controls.append(
                ft.Text(f"La soglia deve essere un numero decimale!", color="red")
            )
            self._view.update_page()
            return
        if floatS<self._pesoMin or floatS>self._pesoMax:
            self._view.lst_result.controls.append(
                ft.Text(f"La soglia deve essere compresa tra {self._pesoMin} e {self._pesoMax}!", color="red")
            )
            self._view.update_page()
            return
        numMin, numMax=self._model.contaArchi(floatS)
        self._view.lst_result.controls.append(
            ft.Text(f"Soglia: {floatS} --> Maggiori {numMax}, minori {numMin}")
        )
        self._view.update_page()

    def handleRicerca(self, e):
        soglia = self._view._txtInN.value
        if soglia == "":
            self._view.lst_result.controls.append(
                ft.Text(f"Inserire valore soglia!", color="red")
            )
            self._view.update_page()
            return
        try:
            floatS = float(soglia)
        except ValueError:
            self._view.lst_result.controls.append(
                ft.Text(f"La soglia deve essere un numero decimale!", color="red")
            )
            self._view.update_page()
            return
        if floatS < self._pesoMin or floatS > self._pesoMax:
            self._view.lst_result.controls.append(
                ft.Text(f"La soglia deve essere compresa tra {self._pesoMin} e {self._pesoMax}!", color="red")
            )
            self._view.update_page()
            return
        path, length=self._model.getBestPath(floatS)
        self._view.lst_result.controls.append(
            ft.Text(f"Migliore sequenza di cromosomi trovata (lunghezza {length}):")
        )
        for c in path:
            self._view.lst_result.controls.append(
                ft.Text(c))
        self._view.update_page()