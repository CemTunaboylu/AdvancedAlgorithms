"""
Minimum Spanning Tree is a subset of edges of a connected, edge weighted undirected graph that connects all the vertices together 
without any cycles and with the minimum possible edge weight. It is a spanning tree whose sum of edge weights is as small as possible.
Generally, every undirected edge-weighted graph(not necessarily connected) has a minimum spanning forest which is a union of the minimum spanning trees
for its connected parts.
If every edge has unique weight, there is only one unique MST.
"""
from collections import namedtuple
point3D = namedtuple("point3D", ["x", "y", "z"])

def neighbors(p:tuple, t:tuple): 
        n_l = []
        for dim, (p_dim, t_dim) in enumerate(zip(p,t)):
                if p[dim] > 0: # as its nature 
                        n = tuple([ p[d] if d!=dim else p[d]-1 for d in range(len(p)) ]) 
                        n_l.append(type(p)(*n))
                if p[dim] < t[dim]:
                        n = tuple([ p[d] if d!=dim else p[d]+1 for d in range(len(p)) ]) 
                        n_l.append(type(p)(*n))
        return n_l

t = point3D(1,1,1)
print(t)
n = neighbors(t, point3D(2,2,2))
# n = tuple([ t[d] if d!=0 else t[d]+1 for d in range(len(t)) ])
# n = point3D(*n)
print(n)
