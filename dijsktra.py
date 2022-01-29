"""
Dijkstra's algorithm, as another example of a uniform-cost search algorithm, can be viewed as a special case of A* where 
h(x) = 0 for all x.[10][11] General depth-first search can be implemented using A* by considering that there is a global counter 
C initialized with a very large value. Every time we process a node we assign C to all of its newly discovered neighbors. 
After each single assignment, we decrease the counter C by one. Thus the earlier a node is discovered, the higher its 
h(x) value. Both Dijkstra's algorithm and depth-first search can be implemented more efficiently without including an 
h(x) value at each node.
"""


            