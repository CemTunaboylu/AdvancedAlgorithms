from collections import namedtuple
from typing import List 
import heapq

Edge = namedtuple("Edge", ["weight, to"])

class Node:
        def __init__(self, _v, n=None, _in_degree=0):
                self.value = _v
                self.in_degree=_in_degree
                self.neighbors = [] # Edges
        def add_neighbor(self, w, n):
                if n:
                        heapq.heappush(self.neighbors, Edge(w, n))
        def lowest_weight_neighbor(self):
                if len(self.neighbors) > 0:
                        return heapq.heappop()
        def set_in_degree(self, i):
                self.in_degree=i

class Graph:
        def __init__(self):
                self.in_degree_zeros = List[Node]
        
        def add_node(self, n):
                self.in_degree_zeros.append(n)



# For Adjacency matrix, if something is visited, we can make it negative ??
        