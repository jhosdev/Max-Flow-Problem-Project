import random
import copy
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Tests graphs with capacity

graph_ex2 = [
    [0, 4, 6, 0, 0, 0],
    [0, 0, 0, 3, 0, 0],
    [0, 4, 0, 4, 3, 0],
    [0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0]
]

graph_ex = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]

class Graph:
 
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)
        # self.COL = len(gr[0])
 
    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''
 
    def bfs(self, s, t, parent):

        visited = [False]*(self.ROW)

        queue = []
 
        queue.append(s)
        visited[s] = True
 
        while queue:
 
            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
 
        return False

    def ford_fulkerson(self, source, sink):

        parent = [-1]*(self.ROW)
 
        max_flow = 0

        all_paths = []
        all_paths_weight = []
        number_of_paths=0

        while self.bfs(source, sink, parent) :
            path_flow = float("Inf")
            s = sink

            path = []

            while(s !=  source):
                path.append(s)
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow +=  path_flow
            v = sink

            number_of_paths += 1

            path.append(source)
            path.reverse()

            all_paths.append(path)
            all_paths_weight.append(path_flow)

            while(v !=  source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
                #print(u)
                #print(v)
 
        print("\nTotal de caminos: ",number_of_paths)
        print("Caminos:")
        for it in range(number_of_paths):
          print(it+1, all_paths[it], "Peso:" ,all_paths_weight[it])

        return max_flow

class Drawing:
    def draw_graph(self, graph, name):
        G = nx.DiGraph()

        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[i][j] != 0:
                    G.add_edge(i, j, capacity=graph[i][j])

        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'capacity'))
        plt.savefig(name)


class UserInterface:
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.choice = None
        self.matrix = None
        self.initial_matrix = None
        self.n = None
        self.source = None
        self.sink = None

    def generate_random_matrix(self, n):
        matrix = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j and j != 0:
                    matrix[i][j] = random.randint(0, 9)
                else:
                    matrix[i][j] = 0

        return matrix
    
    def input_matrix_manually(self, n):
        matrix = []
        print("Ingresa el valor de cada elemento de la matriz.")
        print("0 simboliza que no hay conexion, un valor mayor a 0 establece conexion ademas de almacenar el peso deseado")
        for _ in range(n):
            row = []
            for _ in range(n):
                value = input(f"Enter 1 or 0 for row {_ + 1}, column {_ + 1}: ")
                row.append(int(value))
            matrix.append(row)
        return matrix
    
    def get_rows(self):
        self.n = int(input("Ingrese el tamanio de la matriz: "))

    def get_initial_input(self):
        print('Bienvenido al programa del Flujo Maximo')
        self.choice = input("Selecciona como deseas ingresar la matriz\n'a' para generar la matriz aleatoriamente\n'm' para generarla manualmente\n't' para usar una matriz de prueba\n")

        if self.choice == 'a':
            self.get_rows()
            self.matrix = self.generate_random_matrix(self.n)
            self.initial_matrix = copy.deepcopy(self.matrix)
        elif self.choice == 'm':
            self.get_rows()
            self.matrix = self.input_matrix_manually(self.n)
            self.initial_matrix = copy.deepcopy(self.matrix)
        elif self.choice == 't':
            self.matrix = graph_ex2
            self.initial_matrix = copy.deepcopy(self.matrix)
            self.n = len(self.matrix)
        else:
            print("Option invalida")
            self.get_initial_input()

    def print_matrix(self):
      print("\nMatriz generada:")
      for i, row in enumerate(self.matrix):
          print(f'Vertice {i}:', row)
        
      available_nodes = ', '.join(str(i) for i in range(len(self.matrix)))
      print("Vertices disponibles:", available_nodes)

        

    def print_output(self):
        g= Graph(self.matrix)
        initial = Drawing()
        final = Drawing()

        print("\nAhora, seleccione los vertices para calcular el flujo maximo")
        self.source = int(input("Ingresa el vertice de origen: "))
        self.sink = int(input("Ingresa el vertice final: "))

        #initial.draw_graph(self.matrix, 'initial_graph.png')
        #plt.clf()

        print("\nEl flujo maximo es: %d " % g.ford_fulkerson(self.source, self.sink))
        print("\n")
        final.draw_graph(self.initial_matrix, 'initial_graph.png')
 
def main():
    u = UserInterface(5,15)
    u.get_initial_input()
    u.print_matrix()
    u.print_output()
    

if __name__ == "__main__":
    main()