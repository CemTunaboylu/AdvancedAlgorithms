from cmath import sqrt
from collections import namedtuple

from a_star import recursive_dimension_builder, a_star


def get_variables_from_module_named(module_name):
    module = globals().get(module_name, None)
    vars = {}
    if module:
        vars = {key: value for key, value in module.__dict__.items() if not (key.startswith('__') or key.startswith('_'))}
    return vars


cube = [        [[0,1,0],[0,1,1],[1,1,1]],
                [[0,0,1],[1,0,1],[1,1,1]],
                [[1,0,1],[1,0,1],[0,0,0]],
        ]
def recursive_dimension_builder_test():
        other_cube = recursive_dimension_builder(cube, True, 1, False)
        for o in other_cube:
                print(o)

def heuristic(cur, tar):
        d = 0
        for c,t in zip(cur, tar):
                d +=  pow(t-c,2)  
        return sqrt(d) 

point3D = namedtuple("point3D", ["x", "y", "z"])

def neighbors_3D(p, t):
        n_l = []
        if p.x > 0:  
            l = point3D(p.x-1,p.y,p.z)
            n_l.append(l)
        if p.x < t.x:
            r = point3D(p.x+1, p.y, p.z)
            n_l.append(r)
        if p.y > 0:
            d = point3D(p.x, p.y-1, p.z)
            n_l.append(d)
        if p.y < t.y:
            u = point3D(p.x, p.y+1, p.z)
            n_l.append(u)
        if p.z > 0:
            de = point3D(p.x, p.y, p.z-1)
            n_l.append(de)
        if p.z < t.z:
            do = point3D(p.x, p.y, p.z+1)
            n_l.append(do)
        return n_l

point2D = namedtuple("point2D", ["x", "y"])

def neighbors_2D(p, t):
        n_l = []
        if p.x > 0:  
            l = point2D(p.x-1,p.y)
            n_l.append(l)
        if p.x < t.x:
            r = point2D(p.x+1, p.y)
            n_l.append(r)
        if p.y > 0:
            d = point2D(p.x, p.y-1)
            n_l.append(d)
        if p.y < t.y:
            u = point2D(p.x, p.y+1)
            n_l.append(u)
        return n_l

def compare(a_p,b_p):
        for a,b in zip(a_p,b_p):
                if a!=b:
                        return False
        return True

def pos_in_tensor(tensor, a):
        v = tensor
        for coor in a:
                v = v[coor]
        return v

def set_3D_pos_in_tensor(tensor, a, v):
        tensor[a.x][a.y][a.z] = v
def set_2D_pos_in_tensor(tensor, a, v):
        tensor[a.x][a.y] = v

def cube_shortest_path():
        p, t = a_star( 
                point3D(0,0,0),
                point3D(2,2,2),
                cube,
                heuristic,
                1,
                neighbors_3D,
                compare,
                pos_in_tensor,
                set_3D_pos_in_tensor,
                )
        print(p)
        for r in t:
                print(r)

def shortest_paths_2D_matrices():
        ms = get_variables_from_module_named('matrices')
        for k,m in ms.items():
                print(f"Calculating shortest path for :{k}")
                target = point2D(len(m)-1, len(m[0])-1 )
                p, t = a_star( 
                point2D(0,0),
                target,
                m,
                heuristic,
                1,
                neighbors_2D,
                compare,
                pos_in_tensor,
                set_2D_pos_in_tensor,
                )
                print(f"Found : {compare(p, target)}")
if __name__=="__main__":
        # cube_shortest_path()
        import matrices
        shortest_paths_2D_matrices()
