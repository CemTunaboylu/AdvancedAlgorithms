from sys import path
path.append("..")
from Heaps.fib_heap import FibHeap
from typing import List, Union, Any
from enum import Enum
from defaults import *

# Map can be an n-D list or a string representing the 2D space. The navigation on the grid
# is left to the user with a function parameterized here as pos_in_euclidean_n_space_func. Using explicitly obj.x and so on
# would have limited the dimension of the grid that can be fed. Hopefully, this A* search can work on euclidean_n_spaces 
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


INF_INT = pow(2,5)

def form_cost_euclidean_n_space(euclidean_n_space, unwanted, u_value=None, value=INF_INT): # g()
        return recursive_dimension_builder(euclidean_n_space, value, unwanted, u_value)
def form_f_euclidean_n_space(euclidean_n_space, unwanted, u_value=None, value=INF_INT): # f()
        return recursive_dimension_builder(euclidean_n_space, value, unwanted, u_value)
def form_path_euclidean_n_space(euclidean_n_space, unwanted, u_value=None, value=None): # f()
        return recursive_dimension_builder(euclidean_n_space, value, unwanted, u_value)

# Here I assumed that the euclidean_n_space (multi-D matrix) is consistent 
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
                        

def find_path_to_this_node(euclidean_n_space, node, pos_in_euclidean_n_space_func=value_in_euclidean_n_space):
        path = []
        while node != None:
                path.append(node)
                node = pos_in_euclidean_n_space_func(euclidean_n_space, node)
        return path
        
def a_star( start_node, # n-D namedtuple/tuple (x,y,z,...) 
            target_node, # n-D namedtuple/tuple (x,y,z,...) 
            euclidean_n_space, # n-D space 
            unwanted_value,
            compare_func = compare_by_coordinates,
            cost_func = cost,
            key_func_for_fib_heap=default_key_for_node,
            heuristic = Heuristic.EUCLIDEAN, 
            n_d_neighbors = two_n_directional_neighbors_in_n_d_space, # retrieving the neighbors of the current point
            value_in_euclidean_n_space = value_in_euclidean_n_space, 
            set_pos_in_euclidean_n_space = set_pos_in_euclidean_n_space,
            return_path_euclidean_n_space = False
        #     attr_name_for_indication, # example : wall:1, passable:0
             )->Union[Any, List]:
        f_euclidean_n_space = form_f_euclidean_n_space(euclidean_n_space, unwanted_value)
        cost_euclidean_n_space = form_cost_euclidean_n_space(euclidean_n_space, unwanted_value)
        path_euclidean_n_space = form_path_euclidean_n_space(euclidean_n_space, unwanted_value)
        set_pos_in_euclidean_n_space(cost_euclidean_n_space, start_node, 0)
        set_pos_in_euclidean_n_space(f_euclidean_n_space, start_node, heuristic(start_node, target_node))
        priority_queue = FibHeap([start_node], sort_key=key_func_for_fib_heap)
        space_dimensions = discover_space_dimensions(euclidean_n_space)
        while not priority_queue.is_empty():
                current_node = priority_queue.pop_min()
                if compare_func(current_node, target_node):
                        if return_path_euclidean_n_space:
                                return current_node, path_euclidean_n_space
                        return current_node 

                neighbors = n_d_neighbors(current_node, space_dimensions)
                for n in neighbors:
                        if value_in_euclidean_n_space(euclidean_n_space, n) == unwanted_value: # agent cannot navigate through, e.g. a wall   
                                continue
                        g_val = value_in_euclidean_n_space(cost_euclidean_n_space, current_node) + cost_func(n)
                        if g_val < value_in_euclidean_n_space(cost_euclidean_n_space, n): # if the cost of getting to n is bigger than the current path, update
                                set_pos_in_euclidean_n_space(path_euclidean_n_space, n, current_node)
                                set_pos_in_euclidean_n_space(cost_euclidean_n_space, n, g_val)
                                f = (g_val+heuristic(n, target_node))
                                set_pos_in_euclidean_n_space(f_euclidean_n_space, n, f)
                                priority_queue.push(n) # if already here, checks is key is smaller, if so decreases the key?

        if return_path_euclidean_n_space:
                return None, path_euclidean_n_space
        return None
