import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


#class Graph:
def Graph():
    adj_mat = np.loadtxt(r'C:\Users\Connor Moore\Desktop\365 Project Uber\Code\base_files\network.csv', delimiter=',')
    graph_ = nx.from_numpy_matrix(adj_mat, create_using=nx.MultiGraph)
    return graph_

# G = Graph()
# nx.draw(G)
# plt.show()
