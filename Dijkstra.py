import networkx as nx
import numpy as np

def dijkstra(G, source, dest):
    # mark all nodes as unvisited
    # change source distance to 0
    # all others to 10000

