import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import math


class GraphA ():
    def __init__(self):
        self.graph = nx.Graph()
        self.dimension = 50

    #Funcion que define los nodos inicial y final
    def start_end(self, start, end):
        self.start = start
        self.end = end
        self.graph1 = nx.Graph()
        a, b = False,False

        for n in range(self.graph.number_of_nodes()):
            if start == self.graph.nodes[n]['id']:
                a = True
            elif end == self.graph.nodes[n]['id']:
                b = True
                
        if a and b:
            self.graph1.add_node(start, id = self.graph.nodes[start]['id'], pos = self.graph.nodes[start]['pos'])
            self.graph1.add_node(end, id = self.graph.nodes[end]['id'], pos = self.graph.nodes[end]['pos'])
        else:
            print('Nodes not found')


    #Crea el grafo con n: numero de nodos y el radio para determinar las conexiones
    def create_graph(self, n, radio):
        for i in range (n): #Crea los nodos con posiciones x & y aletorias, ambos valores menores a la dimension 
            self.graph.add_node(i, id = i, pos=(random.randint(0,self.dimension),random.randint(0,self.dimension)))
        
        #Busca los nodos que tenga una distancia menor al radio 
        list_edge = nx.geometric_edges(self.graph, radius = radio)
        self.graph.add_edges_from(list_edge)   #agrega las aristas
    
#.---------------------------------------------------------------------------------------------------------------------------------------------------
    #Dibuja el grafo creado
    def draw_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw_networkx_nodes(self.graph, pos, node_size=80)
        nx.draw_networkx_edges(self.graph,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(self.graph, pos, font_size=6, font_family="sans-serif")
        plt.title('Grafo')
        plt.show()


    #Dibuja las diferentes búsquedas 
    def draw_graph_search(self):
        
        pos = nx.get_node_attributes(self.graph, 'pos')

        DFS = self.graph.copy()
        BFS = self.graph.copy()
        HC  = self.graph.copy()
        AS  = self.graph.copy()

        plt.subplot(221)
        nx.draw_networkx_nodes(DFS, pos, node_size=100)
        nx.draw_networkx_edges(DFS,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(DFS, pos, font_size=6, font_family="sans-serif")
        edge_list_dfs = list(nx.utils.pairwise(self.dfs()))
        
        nx.draw_networkx(
            self.graph,
            pos,
            with_labels=False,
            edgelist=edge_list_dfs,
            edge_color="red",
            node_size=100,
            width=0.8,
        )
        nx.draw_networkx_nodes(DFS, pos, node_size=100, nodelist=[self.start,self.end], node_color="tab:orange")
        plt.title('Busqueda por Profundidad')
        
        plt.subplot(222)
        nx.draw_networkx_nodes(BFS, pos, node_size=100)
        nx.draw_networkx_edges(BFS,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(BFS, pos, font_size=6, font_family="sans-serif")

        edge_list_bfs = list(nx.utils.pairwise(self.bfs()))

        nx.draw_networkx(
            BFS,
            pos,
            with_labels=False,
            edgelist=edge_list_bfs,
            edge_color="green",
            node_size=100,
            width=0.8,
        )
        nx.draw_networkx_nodes(BFS, pos, node_size=100, nodelist=[self.start,self.end], node_color="tab:orange")
        plt.title('Busqueda por Amplitud')
        
        
        plt.subplot(223)
        nx.draw_networkx_nodes(HC, pos, node_size=100)
        nx.draw_networkx_edges(HC,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(HC, pos, font_size=6, font_family="sans-serif")
        edge_list_hc  = list(nx.utils.pairwise(self.hc()))
        nx.draw_networkx(
            HC,
            pos,
            with_labels=False,
            edgelist=edge_list_hc,
            edge_color="brown",
            node_size=100,
            width=0.8,
        )
        nx.draw_networkx_nodes(HC, pos, node_size=100, nodelist=[self.start,self.end], node_color="tab:orange")
        plt.title('Hill Climbing')


        plt.subplot(224)
        nx.draw_networkx_nodes(AS, pos, node_size=100)
        nx.draw_networkx_edges(AS,pos,edge_color='gray',width = 0.5)
        nx.draw_networkx_labels(AS, pos, font_size=6, font_family="sans-serif")
        edge_list_A_s  = list(nx.utils.pairwise(self.A_start()))
        nx.draw_networkx(
            AS,
            pos,
            with_labels=False,
            edgelist=edge_list_A_s,
            edge_color="blue",
            node_size=100,
            width=0.5,
        )
        nx.draw_networkx_nodes(AS, pos, node_size=100, nodelist=[self.start,self.end], node_color="tab:orange")
        plt.title('A *')
        plt.show()


#------------------------------------------------------------------------------------------------------------------------------------
    #Busqueda en profundidad
    def dfs(self):
        counter = 0
        max = 0
        Route = []
        Stack = []
        Stack.append(self.graph.nodes[self.start])
        
        while Stack:


            counter = counter + 1
            if max < len(Stack):
                max = len(Stack)


            Node_temp = Stack[0]
            if Stack[0]['id'] == self.graph1.nodes[self.end]['id']:
                Route.append(Node_temp['id'])
                print('Busqueda en Amplitud')
                print("Pasos: " + str( counter))
                print("Memoria Max: " + str( max))
                print('-------------------')
                return Route

            del Stack[0]
            
            if Node_temp['id'] not in Route:
                Route.append(Node_temp['id'])
                child = [n for n in nx.all_neighbors(self.graph,Node_temp['id'])]
                for n in child:
                    Stack.insert(0,self.graph.nodes[n])

    #Busqueda por amplitud
    def bfs(self):
        max = 0
        counter = 0
        Route = []
        Queue = []
        Queue.append(self.graph.nodes[self.start])

        while Queue:

            counter = counter + 1
            if max < len(Queue):
                max = len(Queue)
            
            Node_temp = Queue[0]
            if Queue[0]['id'] == self.graph1.nodes[self.end]['id']:
                Route.append(Node_temp['id'])
                print('Busqueda en Profundidad')
                print("Pasos: " + str( counter))
                print("Memoria Max: " + str( max))
                print('-------------------')
                return Route
            
            del Queue[0]

            if Node_temp['id'] not in Route:
                Route.append(Node_temp['id'])
                child = [n for n in nx.all_neighbors(self.graph,Node_temp['id'])]
                for n in child:
                    Queue.append(self.graph.nodes[n])
          
    #Ecludian
    def heuristic(self, Ax,Ay, Bx,By):
        return math.sqrt(pow(Bx - Ax,2) + pow(By - Ay,2))

    #Busqueda Hill Climbing
    def hc(self):
        counter = 0
        Route = []
        Stack = []
        distance = []
        Stack.append(self.graph.nodes[self.start])

        while Stack:

            counter = counter + 1

            Node_temp = Stack[0]
            if Stack[0]['id'] == self.graph1.nodes[self.end]['id']:
                Route.append(Node_temp['id'])
                costo = self.Costo_Camino(Route)
                print('Hill Climbing')
                print("Pasos: " + str(counter))
                print("Costo: " + str(costo))
                print('-------------------')
                return Route

            del Stack[0]

            if Node_temp['id'] not in Route:
                Route.append(Node_temp['id'])
                child = [n for n in nx.all_neighbors(self.graph,Node_temp['id'])]
                for n in child:
                    dis = self.heuristic(self.graph.nodes[n]['pos'][0],self.graph.nodes[n]['pos'][1],self.graph.nodes[self.end]['pos'][0],self.graph.nodes[self.end]['pos'][1])
                    distance.append((self.graph.nodes[n]['id'],dis))

                ordenados = sorted(distance, key=lambda weight: weight[1])

                for x in reversed(ordenados):
                    Stack.insert(0,self.graph.nodes[x[0]])


    def A_start(self):
        counter = 0
        Route = []
        openList = []
        distance = [] #funcion de evaluacion
        openList.append(self.graph.nodes[self.start])

        while openList:

            counter = counter + 1

            current = openList[0]
            if openList[0]['id'] == self.graph1.nodes[self.end]['id']:
                Route.append(current['id'])
                costo = self.Costo_Camino(Route)
                print('A *')
                print("Pasos: " + str(counter))
                print("Costo: " + str(costo))
                print('-------------------')
                return Route

            del openList[0]

            if current['id'] not in Route:
                Route.append(current['id'])

                child = [n for n in nx.all_neighbors(self.graph,current['id'])]
                for n in child:
                    h = self.heuristic(self.graph.nodes[n]['pos'][0],self.graph.nodes[n]['pos'][1],self.graph.nodes[self.end]['pos'][0],self.graph.nodes[self.end]['pos'][1])
                    g = self.heuristic(self.graph.nodes[n]['pos'][0],self.graph.nodes[n]['pos'][1],current['pos'][0],current['pos'][1])
                   
                
                    distance.append((self.graph.nodes[n]['id'],h+g))

                ordenados = sorted(distance, key=lambda weight: weight[1])

                for x in reversed(ordenados):
                    openList.insert(0,self.graph.nodes[x[0]])

    def Costo_Camino(self,route):
        costo = 0

        for x in range (len(route)-1):
            g = self.heuristic(self.graph.nodes[route[x]]['pos'][0],self.graph.nodes[route[x]]['pos'][1] , self.graph.nodes[route[x+1]]['pos'][0],self.graph.nodes[route[x+1]]['pos'][1])
            costo = costo + g
        return costo


def Start():    
    Grafo = GraphA()
    nodos = int(input('Ingrese Número de Nodos: \n'))
    radio = int(input('Ingrese el Radio: \n'))
    Grafo.create_graph(nodos,radio)
    Grafo.draw_graph()

    node_i = int(input('Nodo Inicial: \n'))
    node_f = int(input('Nodo Final: \n'))
    Grafo.start_end(node_i,node_f)
    Grafo.draw_graph_search()



Start()
