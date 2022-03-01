from math import sqrt
from typing import List, Tuple
from limiter import StaticTypeImposed

class Global_Statics:
        N_D_SPACE = StaticTypeImposed(List, None) 
        def __init__(self, space) -> None:
            self.N_D_SPACE = space

GLOBAL_STATICS = None

def set_n_d_space_global(to_this:List):
        global GLOBAL_STATICS
        GLOBAL_STATICS = Global_Statics(to_this)

def print_n_d():
        print(GLOBAL_STATICS.N_D_SPACE)

def default_key_for_node(node:Tuple):
        return value_in_euclidean_n_space(GLOBAL_STATICS.N_D_SPACE, node)

def compare_by_coordinates(a_p:tuple, b_p:tuple):
        for a,b in zip(a_p,b_p):
                if a!=b:
                        return False
        return True

def cost(*args, **kwargs):
        return 1
        
# Default Heuristics
# To Do: 
# Hamming Distance -> needs additional mechanics on tensors?
def euclidean_distance(cur:tuple, tar:tuple):
        d = 0
        for c,t in zip(cur, tar):
                d +=  pow(abs(t-c),2)  
        return sqrt(d) 

def manhattan_distance(cur:tuple, tar:tuple):
        d = 0
        for c,t in zip(cur, tar):
                d +=  abs((t-c))
        return sqrt(d) 
def minkowski_distance(cur:tuple, tar:tuple, p):
        d = 0
        for c,t in zip(cur, tar):
                d += pow(abs(t-c),p)
        return pow(d, 1/p)

def value_in_euclidean_n_space(n_d_space:List, a:tuple):
        v = n_d_space
        # print("-"*20)
        for coor in a:
                v = v[coor]
        return v

def set_pos_in_euclidean_n_space(n_d_space:List, a:tuple, v):
        d = n_d_space
        for c in range(len(a)-1):
                d = d[a[c]]
        d[a[-1]] = v

def discover_space_dimensions(n_d_space:List):
        dims = []
        space = n_d_space
        while isinstance(space, list):
                # because we start from 0 when indexing
                dims.append(len(space)-1)
                space = space[0]
        
        return dims

def two_n_directional_neighbors_in_n_d_space(p:tuple, space_dims:tuple): 
        n_l = []
        for dim, (p_dim, s_dim) in enumerate(zip(p,space_dims)):
                if p[dim] > 0: # as its nature 
                        n = tuple([ p[d] if d!=dim else p[d]-1 for d in range(len(p)) ]) 
                        n_l.append(type(p)(*n))
                if p_dim < s_dim:
                        n = tuple([ p[d] if d!=dim else p[d]+1 for d in range(len(p)) ]) 
                        n_l.append(type(p)(*n))
        return n_l

from types import FunctionType

def dim_test():
        def get_variables_from_module_named(module_name):
                module = globals().get(module_name, None)
                vars = {}
                if module:
                        vars = {key: value for key, value in module.__dict__.items() if not (key.startswith('__') or key.startswith('_') or isinstance(value, FunctionType)) }
                return vars
        n = "two_d_spaces"
        ms = get_variables_from_module_named(n)
        for m in ms:
                d = discover_space_dimensions(ms[m])
                print(F"dimensions of {m} : {d}")

        from spaces.four_d_spaces import elemental_tesseract
        d = discover_space_dimensions(elemental_tesseract)
        print(F"dimensions of elemental_tesseract : {d}")

if __name__ == "__main__":
        from spaces import two_d_spaces
        dim_test()