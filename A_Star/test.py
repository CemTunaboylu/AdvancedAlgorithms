
from collections import namedtuple

from defaults import compare_by_coordinates as compare
from a_star import recursive_dimension_builder, a_star, find_path_to_this_node
from types import FunctionType

def get_variables_from_module_named(module_name):
    module = globals().get(module_name, None)
    vars = {}
    if module:
        vars = {key: value for key, value in module.__dict__.items() if not (key.startswith('__') or key.startswith('_') or isinstance(value, FunctionType)) }
    return vars

def recursive_dimension_builder_test():
        other_cube = recursive_dimension_builder(cube, True, 1, False)
        for o in other_cube:
                print(o)


point4D = namedtuple("point4D", ["x", "y", "z", "w"])
from spaces.four_d_spaces import elemental_tesseract as tesseract
def four_d_shortest_path():
        target = point4D(1,1,1,1)
        p, t = a_star( 
                point4D(0,0,0,0),
                target,
                tesseract,
                1,
                return_path_euclidean_n_space=True
                )
        assert compare(p, target)
        path = find_path_to_this_node(t, p)
        sols = [[ point4D(1,1,1,1), point4D(1,1,1,0), point4D(1,1,0,0), point4D(0,1,0,0), point4D(0,0,0,0) ],
                [ point4D(1,1,1,1), point4D(1,0,1,1), point4D(0,0,1,1), point4D(0,0,0,1), point4D(0,0,0,0) ],
                [ point4D(1,1,1,1), point4D(1,1,1,0), point4D(1,1,0,0), point4D(1,0,0,0), point4D(0,0,0,0) ]
                ]
        # print(f"Found {path}")
        # print(f"sols : {sols}")
        print(f"Found {sols.index(path)}. path : {path}")
        assert path in sols



point3D = namedtuple("point3D", ["x", "y", "z"])
from spaces.three_d_spaces import cube, unit_cube

def three_d_shortest_path():
        target = point3D(2,2,2)
        p, t = a_star( 
                point3D(0,0,0),
                target,
                cube,
                1,
                return_path_euclidean_n_space=True
                )
        assert compare(p, target)
        path = find_path_to_this_node(t, p)
        sol = [point3D(x=2, y=2, z=2), point3D(x=2, y=2, z=1), point3D(x=2, y=1, z=1), point3D(x=1, y=1, z=1), point3D(x=1, y=0, z=1), point3D(x=1, y=0, z=0), point3D(x=0, y=0, z=0)]
        assert sol==path

        target = point3D(1,1,1)
        p, t = a_star( 
                point3D(0,0,0),
                target,
                unit_cube,
                1,
                return_path_euclidean_n_space=True
                )
        assert compare(p, target)
        path = find_path_to_this_node(t, p)
        sol = [point3D(x=1, y=1, z=1), point3D(x=1, y=0, z=1), point3D(x=0, y=0, z=1), point3D(x=0, y=0, z=0)]
        assert sol==path

point2D = namedtuple("point2D", ["x", "y"])

mod_for_2d = "two_d_spaces"

def two_d_shortest_path():
        from time import time
        ms = get_variables_from_module_named(mod_for_2d)
        for k,m in ms.items():
                target = point2D(len(m)-1, len(m[0])-1 )
                p, t = a_star( 
                point2D(0,0),
                target,
                m,
                1,
                return_path_euclidean_n_space=True
                )
                if p:
                        assert compare(p, target)
                

def bottle_neck_test():
        from time import time
        ms = get_variables_from_module_named(mod_for_2d)
        giant = ms['giant']
        R = 100
        times = [None]*R
        for i in range(R):
                now = time()
                target = point2D(len(giant)-1, len(giant[0])-1 )
                p = a_star( 
                point2D(0,0),
                target,
                giant,
                1,
                )
                if p:
                        assert compare(p, target)
                times[i] = time()-now
        avg_time = sum(times)/R
        # print(F"It took {avg_time} for giant {(target.x, target.y)} {len(ms.items())} tests {R} times.")

def no_shortest_path_2D():
        ms = get_variables_from_module_named(mod_for_2d)
        ms = { m:ms[m] for m in ms if "no_path" in m }
        for n,m in ms.items():
                target = point2D(len(m)-1, len(m[0])-1 )
                p, t = a_star( 
                        point2D(0,0),
                        target,
                        m,
                        1,
                        return_path_euclidean_n_space=True
                        )
                assert p==None

def namedtuple_repr(self):
        return "("+str(self.x) + ","+str(self.y) + ","+str(self.z) + ")"
namedtuple.__repr__ = namedtuple_repr

if __name__=="__main__":
        three_d_shortest_path()
        from spaces import two_d_spaces
        two_d_shortest_path()
        no_shortest_path_2D()
        bottle_neck_test()
        four_d_shortest_path()