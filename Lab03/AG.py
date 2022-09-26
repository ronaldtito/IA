import array
from turtle import width
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import math
from scipy.spatial import distance
from scipy.interpolate import interp1d

#---------- Inicializacion -------------
class GraphA ():
    def __init__(self):
        self.graph = nx.Graph()
        self.dimension = 50
     
    def create_graph(self, n):
        self.n = n
        for i in range (n): 
            self.graph.add_node(i, id = i, pos=(random.randint(0,self.dimension),random.randint(0,self.dimension)))
         
        list_edge = nx.geometric_edges(self.graph, radius = self.dimension)
        self.graph.add_edges_from(list_edge)    


        self.start = 0 

    def numRam(self,min, max):
        num = random.randint(min, max)
        return num

    def generarPoblacion(self , numIndividuos):
        PI = []

        for p in range(0,numIndividuos):
            Individuo = []
            Individuo.append(self.start)
            i = 1

            while i != self.n:
                indi = self.numRam(1,self.n-1)
                if indi not in Individuo:
                    Individuo.append(indi)
                    i=i+1
            Individuo.append(self.start)
            PI.append(Individuo)
        
        return PI
#----------- Graficos ---------------
    def draw_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw_networkx_nodes(self.graph, pos, node_size=80)
        nx.draw_networkx_edges(self.graph,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(self.graph, pos, font_size=6, font_family="sans-serif")
        plt.title('Grafo')
        plt.show()

    def Solution(self,ruta,media,mejor,generation):
        pos = nx.get_node_attributes(self.graph, 'pos')
        CV = self.graph.copy()

        plt.plot()
        nx.draw_networkx_nodes(CV, pos, node_size=80)
        nx.draw_networkx_edges(CV,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(CV, pos, font_size=6, font_family="sans-serif")
        Route = list(nx.utils.pairwise(ruta))

        nx.draw_networkx(
            self.graph,
            pos,
            with_labels=False,
            edgelist = Route,
            edge_color='red',
            node_size=100,
            width=0.8,
        )
        plt.title('Mejor Ruta')
        plt.show()
        plt.plot()

        mejores =  interp1d(generation,mejor,kind ='linear')
        medias = interp1d(generation,media, kind= 'linear')
        plt.plot(generation,mejores(generation),'-',generation,medias(generation),'--')
        plt.legend(['Mejores Rutas','Media de Rutas'])
        plt.title('Mejor and Media')

        plt.suptitle('AG')
        plt.show()
#--------------- Funciones  --------------

    def Ranking(self, P_I):
        ranking = []
        for i in range(len(P_I)):
            Costo = 0
            Route = list(nx.utils.pairwise(P_I[i]))
            for n in range(len(Route)):
                currentCity = Route[n][0]
                neighbourCity = Route[n][1]
                Costo += distance.euclidean(self.graph.nodes[currentCity]['pos'],self.graph.nodes[neighbourCity]['pos'])
            ranking.append((i,int(Costo)))
        ranking = sorted(ranking, key=lambda weight: weight[1])
        return ranking

    def mutacionBasadoPos(self, arr,mutation):
        for a in range(len(arr)):
            if (random.random()<mutation):
                b = int(random.random() * len(arr)-1)
                n1 = arr[a]
                n2 = arr[b]
                arr[a] = n1
                arr[b] = n2
        return arr
    def generarBits(self,arr,n):
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
        bits = []
        self.generarBits(bits,len(arr1))
        #bits = [1,0,1,1,0]
        size = len(arr1)
        tem1 = []
        self.cargarArray(tem1, size + 1)
        tem2 = []
        self.cargarArray(tem2, size + 1)
        tem1[0] = arr1[0]
        tem1[size - 1] = arr1[size - 1]
        tem2[0] = arr2[0]
        tem2[size - 1] = arr2[size - 1]
	
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

    def Cruzamiento_Poblacion(self,poblacion,elitismo):
        Hijos = []
        for i in range(elitismo):
            Hijos.append(poblacion[i])
        

        i = elitismo
        cont = elitismo

        while cont <len(poblacion):
            padre = self.numRam(elitismo,len(poblacion)-1)
            if padre != i:
                hijo = self.cruzamiento(poblacion[i],poblacion[padre])
                Hijos.append(hijo[0])
                Hijos.append(hijo[1])
                i += 1
                cont +=2

        return Hijos

    def selection(self, popRanked,elitismo):
        popSelect = []

        #Elitismo
        for i in range(0,elitismo):
            popSelect.append(popRanked[i][0])
        
        df = pd.DataFrame(np.array(popRanked), columns=['idx','FA'])
        df['cum_sum'] = df.FA.cumsum()
        df['cum_perc'] = 100*df.cum_sum / df.FA.sum()

        #Padres
        for i in range(len(popRanked)- elitismo):
            pick = 100*random.random()
            for n in range(0,len(popRanked)):
                if pick <= df.iat[n,3]:
                    popSelect.append(popRanked[i][0])
                    break
        return popSelect

    def nextGeneration(self, currentPoblation, elitismo,mutation):
        popRanked = self.Ranking(currentPoblation)
        popSelect = self.selection(popRanked,elitismo)

        Hijos = []
        for i in range(len(popSelect)):
            Hijos.append(currentPoblation[popSelect[i]])

        Hijos = self.Cruzamiento_Poblacion(Hijos,elitismo)

        #Mutacion
        NextG = []
        for indv in range(len(Hijos)):
            mutatedIndv = self.mutacionBasadoPos(Hijos[indv],mutation)
            NextG.append(mutatedIndv)
        return NextG

    
        
#------------- Principal --------------------
    def AG(self,CantCiudades,numGeneraciones,numIndividuos,elitismo,mutation):
        
        self.create_graph(CantCiudades)
        self.draw_graph()
        Poblacion = self.generarPoblacion(numIndividuos)

        generation = []
        media = []
        mejor = []
        suma = []
        Population1 = self.Ranking(Poblacion)

        mejor.append(Population1[0][1])
        media.append(sum(j for i, j in Population1)/len(Population1))
        generation.append(0)

    
        for i in range(numGeneraciones):
            Poblacion = self.nextGeneration(Poblacion,elitismo,mutation)
            Population = self.Ranking(Poblacion)
            mejor.append(Population[0][1])
            media.append(sum(j for i, j in Population)/len(Population))
            generation.append(i+1)

        
        

        BestRuta = self.Ranking(Poblacion)

        self.Solution(Poblacion[BestRuta[0][0]],media,mejor,generation)


def Start():
    numeroCiudades = 10
    numeroGeneraciones = 60
    numeroIndividuos = 40
    elitismo =4
    mutation = 0.02

    AgenteViajero = GraphA()
    AgenteViajero.AG(numeroCiudades,numeroGeneraciones,numeroIndividuos,elitismo,mutation)


Start()