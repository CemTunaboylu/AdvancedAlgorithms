from cmath import sqrt

def compare_by_coordinates(a_p, b_p):
        for a,b in zip(a_p,b_p):
                if a!=b:
                        return False
        return True

def cost(*args, **kwargs):
        return 1
        
# Default Heuristics
# To Do: 
# Hamming Distance -> needs additional mechanics on tensors?
def euclidean_distance(cur, tar):
        d = 0
        for c,t in zip(cur, tar):
                d +=  pow(t-c,2)  
        return sqrt(d) 

def manhattan_distance(cur, tar):
        d = 0
        for c,t in zip(cur, tar):
                d +=  abs((t-c))
        return sqrt(d) 
def minkowski_distance(cur, tar, p):
        d = 0
        for c,t in zip(cur, tar):
                d += pow(abs(t-c),p)
        return pow(d, 1/p)

def pos_in_tensor(tensor, a):
        v = tensor
        for coor in a:
                v = v[coor]
        return v

def set_pos_in_tensor(tensor, a, v):
        d = tensor
        for c in range(len(a)-1):
                d = d[a[c]]
        d[a[-1]] = v

def two_n_directional_neighbors_in_n_d_space(p:tuple, t:tuple): 
        n_l = []
        for dim, (p_dim, t_dim) in enumerate(zip(p,t)):
                if p[dim] > 0: # as its nature 
                        n = tuple([ p[d] if d!=dim else p[d]-1 for d in range(len(p)) ]) 
                        n_l.append(type(p)(*n))
                if p[dim] < t[dim]:
                        n = tuple([ p[d] if d!=dim else p[d]+1 for d in range(len(p)) ]) 
                        n_l.append(type(p)(*n))
        return n_l