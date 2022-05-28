"""
Dijkstra's algorithm, as another example of a uniform-cost search algorithm, can be viewed as a special case of A* where 
h(x) = 0 for all x. General depth-first search can be implemented using A* by considering that there is a global counter 
C initialized with a very large value. Every time we process a node we assign C to all of its newly discovered neighbors. 
After each single assignment, we decrease the counter C by one. Thus the earlier a node is discovered, the higher its 
h(x) value. Both Dijkstra's algorithm and depth-first search can be implemented more efficiently without including an 
h(x) value at each node.
"""
from binary_heap import BinaryHeap
from typing import List

not_set_val = float('inf')
# for the sake of simplicity, nodes are numbered {0, ..., num_nodes-1}
def form_graph_matrix(num_nodes:int, directed_graph_weights:List[List[int,int,int]]):
    rows = [None]*num_nodes
    for i in range(num_nodes):
        rows[i] = [not_set_val]*num_nodes

    for weight in directed_graph_weights:
        from_node, to_node, w = weight
        if from_node >= num_nodes or to_node >= num_nodes: raise ValueError(f'{from_node if from_node >= num_nodes else to_node } is out of bounds')
        if w <= 0: raise ValueError(f"weight from {from_node} to {to_node} is '{w}', weights cannot be 0 or smaller.")
        rows[from_node][to_node] = w

    return rows

def form_sample_weights():
    w = [
        [1,3,9],    
        [1,2,7],    
        [1,6,14],    
        [3,6,2],    
        [3,4,11],    
        [2,4,15],    
        [4,5,6],    
        [5,6,9]    
    ]
    return w

# def __init__(self, elms:List=[], comp_method:Callable= __lt__, assign_key:Callable=assign_key):

def compare_elements_w_priority(elm_1, elm_2)->bool:
    return elm_1[0] < elm_2[0]

def assign_key(elm, new_priority):
    return (new_priority, *elm[1:])

def dijkstra(graph_matrix:List[List], start_node:int):
    l = len(graph_matrix)
    path_weights = [not_set_val]*l
    previous = [None]*l
    priorty_queue = BinaryHeap([(0, start_node)], compare_elements_w_priority, assign_key)

    while priorty_queue:
        priority, node = priorty_queue.pop()
        adj_nodes = [ w for w in graph_matrix[node] if w != not_set_val ] 