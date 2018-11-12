import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    adj_mat = np.loadtxt(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\network.csv', delimiter=',')
    graph_ = nx.from_numpy_matrix(adj_mat)
    return graph_

# This just prints the graph
# guess it's gonna be about finding a the least weighted path, rince and repeat, something like that
G = create_graph()
print("edges in g: ", G.edges(data=True))
print(nx.number_of_nodes(G))
#nx.draw(G)
#plt.show()


