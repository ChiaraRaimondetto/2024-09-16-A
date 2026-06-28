import copy

from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self.idMapN={}
        self._bestc = []
        self.punteggio = 0

    def getCorrectionLat(self):
        return DAO.getRangeLat()
    def getCorrectionLng(self):
        return DAO.getRangeLng()
    def getAllShape(self):
        return DAO.getAllShape()
    def buildGraph(self,lat,lng,forma):
        self.grafo.clear()
        nodi=DAO.getAllNodes(lat,lng,forma)
        for n in nodi:
            self.idMapN[n.id]=n
        self.grafo.add_nodes_from(nodi)
        self.addEdges(lat,lng,forma,self.idMapN)
    def addEdges(self,lat,lng,forma,idMapN):
        archi=DAO.getAllEdges(lat,lng,forma,idMapN)
        for a in archi:
            self.grafo.add_edge(a.s1,a.s2,weight=a.peso)
    def getInfo(self):
        nodi=[]
        for n in self.grafo.nodes:
            nodi.append((n.Name,self.grafo.degree(n)))
        nOrdinati=sorted(nodi,key=lambda x:x[1],reverse=True)
        archi=[]
        for u,v,data in self.grafo.edges(data=True):
            archi.append((u.Name,v.Name,data['weight']))
        ordinati=sorted(archi,key=lambda x:x[2],reverse=True)
        return len(self.grafo.nodes),len(self.grafo.edges),nOrdinati[:5],ordinati[:5]


    def bestCammino(self):
        self._bestc=[]
        self.punteggio=0

        for n in self.grafo.nodes:
            parziale=[n]
            self.ricorsione(parziale)
            parziale.pop()
        stampa=[]
        for s in self._bestc:
            stampa.append((s.Name,s.Population))

        return stampa,self.punteggio

    def ricorsione(self,parziale):

        if self.calcolaPunti(parziale)>self.punteggio:
            self.punteggio=self.calcolaPunti(parziale)
            self._bestc=copy.deepcopy(parziale)


        for n in self.grafo.neighbors(parziale[-1]):
            if n not in parziale and n.Population>parziale[-1].Population:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()
    def calcolaPunti(self,parziale):
        pesi=0.0
        distanza=0.0
        if len(parziale)<2:
            return 0
        for i in range(0,len(parziale)-1):
            pesi+=float(self.grafo[parziale[i]][parziale[i+1]]['weight'])
            distanza+=float(parziale[i].distance_HV(parziale[i+1]))
        punti=0
        if distanza!=0:
            punti=float(pesi/distanza)
        return punti



