
import random
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

# This class represents a directed graph
# using adjacency matrix representation
class Graph:
 
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)
        # self.COL = len(gr[0])
 
    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''
 
    def bfs(self, s, t, parent):
 
        # Mark all the vertices as not visited
        visited = [False]*(self.ROW)
 
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True
 
         # Standard BFS Loop
        while queue:
 
            # Dequeue a vertex from queue and print it
            u = queue.pop(0)
 
            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                      # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True
 
        # We didn't reach sink in BFS starting
        # from source, so return false
        return False
             
     
    # Returns the maximum flow from s to t in the given graph
    def ford_fulkerson(self, source, sink):
 
        # This array is filled by BFS and to store path
        parent = [-1]*(self.ROW)
 
        max_flow = 0 # There is no flow initially
 
        # Augment the flow while there is path from source to sink
        while self.bfs(source, sink, parent) :
 
            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while(s !=  source):
                path_flow = min (path_flow, self.graph[parent[s]][s])
                s = parent[s]
 
            # Add path flow to overall flow
            max_flow +=  path_flow
 
            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while(v !=  source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
 
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
        self.n = None
        self.source = None
        self.sink = None

    def generate_random_matrix(self, n):
        matrix = [[0] * n for _ in range(n)]

        # Generate random values for the matrix
        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = random.randint(0, 1)
                else:
                    matrix[i][j] = 0

        return matrix
    
    def input_matrix_manually(self, n):
        matrix = []
        for _ in range(n):
            row = []
            for _ in range(n):
                value = input(f"Enter 1 or 0 for row {_ + 1}, column {_ + 1}: ")
                row.append(int(value))
            matrix.append(row)
        return matrix
    
    def get_rows(self):
        self.n = int(input("Enter the number of rows: "))

    def get_initial_input(self):
        self.choice = input("Enter 'a' to generate a random matrix, 'm' to input data manually or 't' to test with an example matrix: ")

        if self.choice == 'a':
            self.get_rows()
            self.matrix = self.generate_random_matrix(self.n)
        elif self.choice == 'm':
            self.get_rows()
            self.matrix = self.input_matrix_manually(self.n)
        elif self.choice == 't':
            self.matrix = graph_ex2
            self.n = len(self.matrix)
        else:
            print("Invalid input")
            self.get_initial_input()

    def get_source_sink(self):
        self.source = int(input("Enter the source: "))
        self.sink = int(input("Enter the sink: "))

    def print_output(self):

        g= Graph(self.matrix)
        initial = Drawing()
        final = Drawing()

        self.source = int(input("Enter the source: "))
        self.sink = int(input("Enter the sink: "))

        initial.draw_graph(self.matrix, 'initial_graph.png')
        plt.clf()

        print("The maximum possible flow is %d " % g.ford_fulkerson(self.source, self.sink))
        
        final.draw_graph(self.matrix, 'final_graph.png')
 
def main():
    u = UserInterface(5,15)
    u.get_initial_input()
    u.print_output()
    

if __name__ == "__main__":
    main()