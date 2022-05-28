<b>A* search </b> is an informed search algorithm. "Informed" implies that it has information about the goal other than the problem definition i.e. a heuristic function. It operates on best-first bases : it expands the most promising node.
<b> A* search </b> is a graph traversing algorithm for path finding (path on a graph in this case, and is the visited nodes in order from start node to finishing node.).
It is a complete algorithm i.e. it will always find a solution if there is one to be found. 
On finite graphs with non-negative edge weights A* is guaranteed to terminate and is complete.
The space complexity is O(b^d) where b is the number of branches and d is the depth of the tree which is all the possible paths from start to finish (start is the root, finish is the leaves)
<b> A* search </b>  is an extension of Dijkstra's aklgorithm with the difference of an heuristic function - generally an estimation on the distance btw. current and the goal node - guiding the search -hopefully- towards the optimal solution.
It is used mostly on the shortest-path problems - cost is the number of nodes traversed or sum of the weights of the edges used to traverse the path- but can be used in any problem provided that it can satisfy conditions of 
cost algebra.
In each iteration, <b> A* search </b>  tries to minimize the following :
        f(n) = g(n) + h(n) 
        where n is the next node, g(n) is the total cost from start to next node, h(n) is the estimated cost to reach the goal.

<b> A* search </b>  terminates, when node chosen to be expanded is a node that is reached from starting node, or there is no more nodes to expand. Note that the former implies that when the goal reached, we are certain that we reached 
by the shortest path possible. We can be sure of that if and only if the heuristic function h() is 
        a) admissable - never overestimates the actual cost of reaching  the target -
        b) consistent or monotone - h(x) <= d(x,y)+h(y) where d is the length of the edge(x,y)- for the purpose of guaranteeing to find an optimal path without processing any node more than once
        and <b> A* search </b>  is equivalent to running Dijkstra's algorithm with the reduced cost d'(x, y) = d(x, y) + h(y) - h(x).

Typically, a priority queue is used to store the eligable nodes to be expanded i.e. the node with lowest f() value.
Summary of the algorithm:
        Pop the node with the smallest f() from the priority queue
        Update its neighbors f() and g() values, i.e. if current node presents a shorter path from start to that node, update the f() and g() with the new smaller ones. If updated, put them in the priority queue.
        Continue until the popped node is goal node or priority queue is empty.
        If goal is reached, the f() of the goal node is its cost for reaching it from starting node.

Note that we do not know how we got from starting to the goal node, we just know its cost. The algorithm can be modified so that every node keeps track of its predecessor i.e. the shortest path to it from the starting node.
After we find the goal node, we can follow along in reverse until we reach the starting node to get the actual path.

"""