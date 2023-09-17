import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_random_matrix(n):
    matrix = []
    for _ in range(n):
        row = [random.choice([True, False]) for _ in range(n)]
        matrix.append(row)
    return matrix

def input_matrix_manually(n):
    matrix = []
    for _ in range(n):
        row = []
        for _ in range(n):
            value = input(f"Enter 1 or 0 for row {_ + 1}, column {_ + 1}: ")
            row.append(bool(int(value)))
        matrix.append(row)
    return matrix

def create_flow_network(matrix):
    G = nx.DiGraph()
    n = len(matrix)

    # Create nodes for columns (a, b, c, ...)
    for i in range(n):
        G.add_node(chr(ord('a') + i))

    # Add edges based on matrix values
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                G.add_edge(chr(ord('a') + i), chr(ord('a') + j), capacity=1)

    return G


def print_matrix(matrix):
    aux = matrix
    for row in aux:
        print("[", end="")
        for i, val in enumerate(row):
            if (val == True): val = 1
            if (val == False): val = 0
            print(val, end=", " if i < len(row) - 1 else "")
        print("]")


test_matrix = [
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0]
]

def draw_flow_network(flow_network):
    # Create a Kamada-Kawai layout for the directed graph
    pos = nx.kamada_kawai_layout(flow_network)
    nx.draw(flow_network, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    nx.draw_networkx_edge_labels(flow_network, pos, edge_labels=nx.get_edge_attributes(flow_network, 'capacity'))
    plt.title("Flow Network")

    # Save the graph as an image file (e.g., PNG)
    plt.savefig("flow_network.png")




def main():
    """ n = int(input("Enter the number of nodes (n): "))
    choice = input("Enter 'a' to generate a random matrix or 'm' to input data manually: ")

    if choice == 'a':
        matrix = generate_random_matrix(n)
    elif choice == 'm':
        matrix = input_matrix_manually(n)
    else:
        print("Incorrect option")
        return """

    print("Matrix:")
    #print_matrix(matrix)
    print_matrix(test_matrix)

    #flow_network = transform_to_flow_network(matrix)
    flow_network = create_flow_network(test_matrix)
    print("Flow Network:")
    print(flow_network)

    draw_flow_network(flow_network)


if __name__ == "__main__":
    main()
