import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()

        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()} Numero di archi:{self._model.getNumArchi()}"))

        self._view.txt_result.controls.append(ft.Text(f"Informazione sui pesi degli archi- valore minimo: {self._model.valMin} e valore massimo: {self._model.valMax}"))

        self._view.update_page()

    def handle_countedges(self, e):
        self._view.txt_result2.clean()

        self.soglia= self._view.txt_name.value
        #print(soglia)
        try:
            self.fsoglia= float(self.soglia)
        except ValueError:
            self._view.txt_result2.controls.append(ft.Text(f"Inserire un valore numerico"))
            self._view.update_page()
            return


        if self.fsoglia< self._model.valMin  or self.fsoglia> self._model.valMax:
            self._view.txt_result2.controls.append(ft.Text(f"Il valore soglia deve essere compreso fra {self._model.valMin} e {self._model.valMax}"))

        archiinf, archiSup = self._model.getContaArchi(self.fsoglia)
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore alla soglia:{archiSup}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore alla soglia:{archiinf}"))

        self._view.update_page()









    def handle_search(self, e):
        self._model.searchPath(self.fsoglia)
        self._view.txt_result3.clean()
        self._view.txt_result3.controls.append(ft.Text(f" Distanza: {self._model.maxDistanza}"))
        for i in range(len(self._model.bestSol) - 1):
            v1 = self._model.bestSol[i]
            v2 = self._model.bestSol[i + 1]
            self._view.txt_result3.controls.append(ft.Text(f"{v1} ---> {v2}: {self._model._grafo[v1][v2]['weight']}"))
        self._view.update_page()