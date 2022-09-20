import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import math

from main import numRam

class GraphA ():
    def __init__(self):
        self.graph = nx.Graph()
        self.dimension = 50
     
     
     #Crea el grafo con n: numero de nodos y el radio para determinar las conexiones
    def create_graph(self, n):
        self.n = n
        for i in range (n): #Crea los nodos con posiciones x & y aletorias, ambos valores menores a la dimension 
            self.graph.add_node(i, id = i, pos=(random.randint(0,self.dimension),random.randint(0,self.dimension)))
        
        #Busca los nodos que tenga una distancia menor al radio 
        list_edge = nx.geometric_edges(self.graph, radius = self.dimension)
        self.graph.add_edges_from(list_edge)   #agrega las aristas  


        self.graph1 = nx.Graph()
        self.start = 0 #self.graph.nodes[0]['id'] -> Nodo inicial


    def generarPoblacion(self , numIndividuos):
        PI = []

        for p in range(0,numIndividuos):
            Individuo = []
            Individuo.append(self.start)
            i = 1

            while i != self.n:
                indi = self.numRam(1,self.n)
                if indi not in Individuo:
                    Individuo.append(indi)
                    i=i+1
            Individuo.append(self.start)
            PI.append(Individuo)
        
        self.Ranking(PI)
        return PI
    
    def vs(self,comp):
        if(len(comp) == 1):
            return comp
        ganadores = []
        size = len(comp)
        while(size):
            if( comp[0][1] < comp[1][1] ):
                ganadores.append(comp[0])
            else:
                ganadores.append(comp[1])
            comp.pop(0)
            comp.pop(0)
            size -= 2
        return self.vs(ganadores)

    def Torneo(self,T_I):
        comp = T_I
        random.shuffle(comp)
        res = []
        if(len(T_I) % 2): 
            tem = T_I[len(T_I) - 1]
            print(tem)
            print(comp)
            comp.pop(len(T_I) - 1)
            print(comp)
            ganador = vs(comp)
            print(ganador)
            if( ganador[0][1] < tem[1] ):
                return ganador
            else:
                return tem
        else:
            return self.vs(comp)

    def topRuleta(self,currentPoblation):
        return currentPoblation[self.numRam(1,self.n)]


    def nextGeneration(self, currentPoblation):
        topTorneo = self.Torneo(currentPoblation)
        topRuleta = self.Ruleta(currentPoblation)


        Hijos = self.cruzamiento(topTorneo,topRuleta)
        Hijo1 = Hijos[0]
        Hijo2 = Hijos[1]
        self.mutacionBasadaPos(Hijo1)
        self.mutacionBasadaPos(Hijo2)
        #NextG = mutarPoblacion(Hijos)
        NextG = [Hijo1,Hijo2]
        
        return NextG

    #--------------------------------------------- devuleve el mejor costo
    def Ranking(self, P_I):
        rank = []
        #for i in P_I:
        for i in range(len(P_I)-1):
            Costo = 0
            #for n in range(len(i)-2):
            print(P_I[i])
            for n in range(len(P_I[i])-2):
                #print(self.graph.nodes[P_I[i][n]]['id'])
                #print(self.graph.nodes[P_I[i][n+1]]['id'])
                Costo = Costo + int(self.heuristic(self.graph.nodes[P_I[i][n]]['id'],self.graph.nodes[P_I[i][n+1]]['id']))
            P_I_rank = ((i,Costo))
            rank.append(P_I_rank)
        print(rank)
        rank = sorted(rank, key=lambda weight: weight[1])
        print (rank)

        return P_I[rank[0][0]] #debe retornar [(0,costo),(1,costo)])

    def heuristic(self, Ax,Ay, Bx,By):
        return math.sqrt(pow(Bx - Ax,2) + pow(By - Ay,2))

    def heuristic(self, A, B):
        ax =self.graph.nodes[A]["pos"][0]
        ay =self.graph.nodes[A]["pos"][1]
        bx =self.graph.nodes[B]["pos"][0]
        by =self.graph.nodes[B]["pos"][1]
        return math.sqrt(pow(ax-bx,2) + pow(ay-by,2))

#------------------------------------------
    def AG(self,CantCiudades,numGeneraciones,numIndividuos):
        
        self.create_graph(CantCiudades)
        self.draw_graph()
        Poblacion = self.generarPoblacion(numIndividuos)

        for i in range(numGeneraciones):
            Poblacion = self.nextGeneration(Poblacion)

            #Promedio = []
        
        #BestRuta = self.Ranking(Poblacion)
        #return 

   

    def numRam(self,min, max):
        num = random.randint(min, max)
        return num

    def generarBits(self,arr,n):
        print("generando bits")
        i = 0
        while( i < n):
            arr.append(self.numRam(0,1))
            i += 1

    def cargarArray(self,arr, n):
        i = 0
        while (i < n-1):
            arr.append("*")
            i += 1
        
    
    def cruzamiento(self,arr1, arr2):
        print("cruzamiento")
        bits = []
        self.generarBits(bits,len(arr1))
        #bits = [1,0,1,1,0]
        print(bits)
        size = len(arr1)
        tem1 = []
        self.cargarArray(tem1, size + 1)
        tem2 = []
        self.cargarArray(tem2, size + 1)
        tem1[0] = arr1[0]
        tem1[size - 1] = arr1[size - 1]
        tem2[0] = arr2[0]
        tem2[size - 1] = arr2[size - 1]
        print(tem1)
        print(tem2)	
	
        i = 1 
        while(i < size - 1):
            if(bits[i] == 1):
                pos = arr1.index(arr1[i])
			    #print(pos)
                tem1[pos] = arr2[pos]
            i += 1	
        

        for n in arr1:
            if n not in tem1:
                pos = tem1.index('*')
                tem1[pos] = n

        i = 1 
        while(i < size - 1):
            if(bits[i] == 1):
                pos = arr2.index(arr2[i])
			    #print(pos)
                tem2[pos] = arr1[pos]
            i += 1
        i = 1 
        for n in arr2:
            if n not in tem2:
                pos = tem2.index('*')
                tem2[pos] = n	

        return [tem1,tem2]
        """print(tem1)
        print(tem2)"""

     #Dibuja el grafo creado
    
    def mutacionBasadaPos(self,arr):
        print("mutacion")
        n1 = numRam(1, len(arr) - 2)
        n2 = numRam(1, len(arr) - 2)
        while(n1 == n2):
            n2 = numRam(0, len(arr) - 2)
        print(str(n1) + '\t' + str(n2))
        
        tem = arr[n1]
        arr[n1] = arr[n2]
        arr[n2] = tem
    
    def draw_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw_networkx_nodes(self.graph, pos, node_size=80)
        nx.draw_networkx_edges(self.graph,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(self.graph, pos, font_size=6, font_family="sans-serif")
        plt.title('Grafo')
        plt.show()
    #----------------------------------------------------


def Start():    
    Grafo = GraphA()
    #nodos = int(input('Ingrese Número de Nodos: \n'))
    #radio = int(input('Ingrese el Radio: \n'))
    numeroCiudades = 10
    numeroGeneraciones = 20
    numeroIndividuos = 5
    Grafo.AG(numeroCiudades,numeroGeneraciones,numeroIndividuos)
    Grafo.draw_graph()




Start()