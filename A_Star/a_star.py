"""
A* is an informed search algorithm meaning that it has information about the goal other than the problem definition i.e. a heuristic function. It operates on best-first bases meaning that 
it expands the most promising node.
A* search is a graph traversing algorithm for path finding (path on a graph in this case, and is the visited nodes in order from start node to finishing node.).
It is a complete algorithm i.e. it will always find a solution if there is one to be found. 
On finite graphs with non-negative edge weights A* is guaranteed to terminate and is complete.
The space complexity is O(b^d) where b is the number of branches and d is the depth of the tree which is all the possible paths from start to finish (start is the root, finish is the leaves)
A* is an extension of Dijkstra's aklgorithm with the difference of an heuristic function - generally an estimation on the distance btw. current and the goal node - guiding the search -hopefully- towards the optimal solution.
It is used mostly on the shortest-path problems - cost is the number of nodes traversed or sum of the weights of the edges used to traverse the path- but can be used in any problem provided that it can satisfy conditions of 
cost algebra.
In each iteration, A* tries to minimize the following :
        f(n) = g(n) + h(n) 
        where n is the next node, g(n) is the total cost from start to next node, h(n) is the estimated cost to reach the goal.

A* terminates, when node chosen to be expanded is a node that is reached from starting node, or there is no more nodes to expand. Note that the former implies that when the goal reached, we are certain that we reached 
by the shortest path possible. We can be sure of that if and only if the heuristic function h() is 
        a) admissable - never overestimates the actual cost of reaching  the target -
        b) consistent or monotone - h(x) <= d(x,y)+h(y) where d is the length of the edge(x,y)- for the purpose of guaranteeing to find an optimal path without processing any node more than once
        and A* is equivalent to running Dijkstra's algorithm with the reduced cost d'(x, y) = d(x, y) + h(y) - h(x).

Typically, a priority queue is used to store the eligable nodes to be expanded i.e. the node with lowest f() value.
Summary of the algorithm:
        Pop the node with the smallest f() from the priority queue
        Update its neighbors f() and g() values, i.e. if current node presents a shorter path from start to that node, update the f() and g() with the new smaller ones. If updated, put them in the priority queue.
        Continue until the popped node is goal node or priority queue is empty.
        If goal is reached, the f() of the goal node is its cost for reaching it from starting node.

Note that we do not know how we got from starting to the goal node, we just know its cost. The algorithm can be modified so that every node keeps track of its predecessor i.e. the shortest path to it from the starting node.
After we find the goal node, we can follow along in reverse until we reach the starting node to get the actual path.

"""

# Python has a built-in binary-heap module heapq, which we will use as a priority queue

# getattr(obj, "string_repr_of_attribute")
# setattr(obj, attrname, value)
# Note: Comparisons sometimes involve calling user-defined code using .__lt__(). 
# Calling user-defined methods in Python is a relatively slow operation compared with other 
# operations done in a heap, so this will usually be the bottleneck.

import heapq
from typing import List
from enum import Enum
from defaults import *
# Map can be an n-D list or a string representing the 2D space. The navigation on the grid
# is left to the user with a function parameterized here as pos_in_tensor_func. Using explicitly obj.x and so on
# would have limited the dimension of the grid that can be fed. Hopefully, this A* search can work on tensors 
# with all sorts of ranks 


# from dataclasses import dataclass, field
# from typing import Any

# @dataclass(order=True)
# class PrioritizedItem:
#     priority: float
#     item: Any=field #(compare=True)


class Heuristic(Enum):
        EUCLIDEAN = euclidean_distance
        MANHATTAN = manhattan_distance
        MINKOWSKI = minkowski_distance

# INF_INT = pow(2,10000)
INF_INT = pow(2,5)
# __cmp__ methods
def form_cost_tensor(tensor, unwanted, u_value=None, value=INF_INT): # g()
        return recursive_dimension_builder(tensor, value, unwanted, u_value)
def form_f_tensor(tensor, unwanted, u_value=None, value=INF_INT): # f()
        return recursive_dimension_builder(tensor, value, unwanted, u_value)
def form_path_tensor(tensor, unwanted, u_value=None, value=None): # f()
        return recursive_dimension_builder(tensor, value, unwanted, u_value)

# Here I assumed that the tensor (multi-D matrix) is consistent 
# i.e. length of rows of each dimension is the same across the dimension
def recursive_dimension_builder(row, value, unwanted, u_value)->List:
        if len(row)== 0:
                return [None]
        t = []
        for r in row:
                if isinstance(r, list):
                        t.append(recursive_dimension_builder(r, value, unwanted, u_value))
                else:
                        t.append( value if r != unwanted else u_value )
        
        return t
                        

def find_path_to_this_node(tensor, node, pos_in_tensor_func=pos_in_tensor):
        path = []
        while node != None:
                path.append(node)
                node = pos_in_tensor_func(tensor, node)
        return path
        
def a_star( start_node, # n-D namedtuple/tuple (x,y,z,...) 
            target_node, # n-D namedtuple/tuple (x,y,z,...) 
            tensor, # n-D space 
            unwanted_value,
            compare_func = compare_by_coordinates,
            cost_func = cost,
            heuristic = Heuristic.EUCLIDEAN, 
            n_d_neighbors = two_n_directional_neighbors_in_n_d_space, # retrieving the neighbors of the current point
            pos_in_tensor = pos_in_tensor, 
            set_pos_in_tensor = set_pos_in_tensor,
            return_path_tensor = False
        #     attr_name_for_indication, # example : wall:1, passable:0
             ):
        # priority_queue = [PrioritizedItem(0, start_node)]
        priority_queue = [(0, start_node)]
        nodes_set = set()
        nodes_set.add(start_node)
        cost_tensor = form_cost_tensor(tensor, unwanted_value)
        
        set_pos_in_tensor(cost_tensor, start_node, 0)
        f_tensor = form_f_tensor(tensor, unwanted_value)
        set_pos_in_tensor(f_tensor, start_node, heuristic(start_node, target_node))
        path_tensor = form_path_tensor(tensor, unwanted_value)
        while len(priority_queue) > 0:
                # current_node = heapq.heappop(priority_queue).item
                f, current_node = heapq.heappop(priority_queue)
                if compare_func(current_node, target_node):
                        if return_path_tensor:
                                return current_node, path_tensor
                        return current_node 

                neighbors = n_d_neighbors(current_node, target_node)
                for n in neighbors:
                        if pos_in_tensor(tensor, n) == unwanted_value: # agent cannot navigate through, e.g. a wall   
                                continue
                        g_val = pos_in_tensor(cost_tensor, current_node) + cost_func(n)
                        if g_val < pos_in_tensor(cost_tensor, n): # if the cost of getting to n is bigger than the current path, update
                                set_pos_in_tensor(path_tensor, n, current_node)
                                set_pos_in_tensor(cost_tensor, n, g_val)
                                f = (g_val+heuristic(n, target_node))
                                set_pos_in_tensor(f_tensor, n, f )
                                if not n in nodes_set: # bottleneck was checking in heap which is O(n) but it seems heap check is faster?
                                # if not n in priority_queue: # bottleneck was checking in heap which is O(n)
                                        # heapq.heappush(priority_queue, PrioritizedItem(f,n))
                                        heapq.heappush(priority_queue, (f,n))
                                        nodes_set.add(n) # I can have an element pointing to the pos in heap
        if return_path_tensor:
                return None, path_tensor
        return None

# TO DO
# use a set to track if an elm is in the priority_queue
# built_in __cmp__ method in the class ?
# def __cmp__(self, other):
        # return cmp(self.priority, other.priority)