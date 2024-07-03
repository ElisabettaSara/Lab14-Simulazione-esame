import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo= nx.DiGraph()
        self.bestSol=0

    def searchPath(self, sogl):
        self.soglia=sogl
        parziale=[]
        self.maxDistanza=0
        for n in self._grafo.nodes:
            parziale=[n]
            pesi=[0]
            archi_visitati=[]
            self.ricorsione(parziale,pesi,archi_visitati)

    def ricorsione(self, parziale, pesi, archi_visitati):
        last= parziale[-1]
        vicini= sorted(self._grafo[last], key=lambda x: self._grafo[last][x]['weight'] )

        vicini_utilizzabili=[]
        for n in vicini:
            if (last,n) not in archi_visitati and float(self._grafo[last][n]['weight'])>self.soglia:
                vicini_utilizzabili.append(n)

        if len(vicini_utilizzabili)==0:
            distanza = self.calcolaDistanza(parziale)
            if distanza>self.maxDistanza:
                self.maxDistanza=distanza
                self.bestSol = copy.deepcopy(parziale)

        for n in vicini_utilizzabili:
            pesi.append(self._grafo[last][n]['weight'])
            archi_visitati.append((last,n))
            parziale.append(n)

            self.ricorsione(parziale, pesi, archi_visitati)

            pesi.pop()
            archi_visitati.pop()
            parziale.pop()



    def calcolaDistanza(self,parziale):
        distanza = 0.0
        for i  in range(len(parziale)-1):
            v1=parziale[i]
            v2=parziale[i+1]
            distanza+= self._grafo[v1][v2]['weight']
        return distanza






    def buildGraph(self):
        self._grafo.clear()
        zero = 0
        nodi= DAO.getCromosomi(zero)
        self._grafo.add_nodes_from(nodi)

        edges= DAO.getPeso()
        print(len(edges))
        self.valMin=1000000
        self.valMax=0
        m=0
        #self._grafo.add_weighted_edges_from(edges)
        for edge in edges:

            self._grafo.add_edge(edge[0],edge[1], weight=float(edge[2]))

            if edge[2] < self.valMin:
                self.valMin=edge[2]
            if edge[2]> self.valMax:
                self.valMax= edge[2]

        # print(m)
        # print(self.getNumNodi())
        # print(self.valMin)
        # print(self.valMax)
        #self._grafo.add_weighted_edges_from(DAO.getPeso())


    # def getMin(self):
    #     for edge in self._grafo.edges:
    #         print(edge['weight'])



    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getContaArchi(self, fsoglia):
        sogliaMinore=0
        sogliaMaggiore=0
        for edge,weight in nx.get_edge_attributes(self._grafo, 'weight').items():
            if weight<fsoglia:
                sogliaMinore+=1
            if weight>fsoglia:
                sogliaMaggiore+=1
        return sogliaMinore, sogliaMaggiore


