try:
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import numpy as np
except Exception as e:
        print(e)

from typing import List
from itertools import product
from sys import path
path.append("..")
from A_Star.defaults import value_in_euclidean_n_space

# Get the space as a parameter
#       - get space_dims correctly
#       - extract each wall point
#       - put a box at the positions of each wall point (adjust the alpha)
#       - make the path ticker

def plot_space(path:List, space, space_dim, start, target, title): 
        
        dimensions = tuple(zip(*path))
        fig = plt.figure(figsize=(4,4))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(title)

        extract_walls(space, space_dim, 1)

        # gender_labels = np.random.choice([0, 1], 35) #0 for male, 1 for female
        # ax.scatter(xs = heights, ys = weights, zs = ages, c=gender_labels)
        # print(f"gender: {gender_labels}")

        # colorbar 
        # scat_plot = ax.scatter(xs = heights, ys = weights, zs = ages, c=gender_labels)
        # cb = plt.colorbar(scat_plot, pad=0.2)
        # cb.set_ticks([0,1])
        # cb.set_ticklabels(["Male", "Female"])

        #ax.grid(False)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        ax.set_ylim(0,2)
        ax.set_zlim(0,2)
        ax.set_xlim(0,2)

        ax.set_xticks( range(0,space_dim[0]) )
        ax.set_yticks( range(0,space_dim[1]) )
        ax.set_zticks( range(0,space_dim[2]) )

        # ax.scatter(2,3,4) # plot the point (2,3,4) on the figure
        # ax.plot(x,y,z)
        ax.scatter(*start)
        ax.scatter(*target)
        walls = extract_walls(space, space_dim, 1)
        cube(ax, space, space_dim)
        # cuboid(ax)
        ax.plot(*dimensions)


        plt.show()

def cuboid(ax):
        # prepare some coordinates
        x, y, z = np.indices((8, 8, 8))
        print(f"x : {x }")

        # draw cuboids in the top left and bottom right corners, and a link between
        # them
        cube1 = (x < 3) & (y < 3) & (z < 3)
        print(f"cube1 : {cube1}")
        cube2 = (x >= 5) & (y >= 5) & (z >= 5)
        link = abs(x - y) + abs(y - z) + abs(z - x) <= 2
        print(f"link : {link}")

        # combine the objects into a single boolean array
        voxelarray = cube1 | cube2 | link
        print(f"voxelarray : {voxelarray}")

        # set the colors of each object
        colors = np.empty(voxelarray.shape, dtype=object)
        colors[link] = 'red'
        colors[cube1] = 'blue'
        colors[cube2] = 'green'

        # and plot everything
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

        # plt.show()

def cube(ax, space, space_dim):
        # Control colour
        alpha = 0.6
        x,y,z = np.indices(space_dim)

        print(f"x : {x}")

        cube_1 = (x>0) & (y>0) & (z>0)
        cube_2 = (x<1) & (y<1) & (z<1)
        cube_3 = (x>0) & (y<1) & (z<1)

        voxelarray = cube_1 | cube_2 | cube_3
        print(f"cube_1 : {cube_1}" )
        print(f"cube_2 : {cube_2}" )
        print(f"cube_3 : {cube_3}" )
        # coordinates = np.ones([ w+1 for w in walls[0]], dtype=np.bool)
        # print(f"coor : {coordinates} for the wall {walls[0]}")
        # colors = np.empty(walls[0] + [4], dtype=np.float32)        
        colors = np.empty(list(voxelarray.shape) + [4], dtype=object)
        colors[cube_1] = [1, 0, 0, alpha]
        colors[cube_2] = [1, 1, 1, alpha]
        colors[cube_3] = [0, 0, 1, alpha]
  
        # colors[:] = [1, 1, 1, alpha]  # gray
        ax.voxels(voxelarray, facecolors=colors)
        # for w in walls:                
        #         colors = np.empty(space_dim + [4], dtype=np.float32)        
        #         colors[:] = [1, 1, 1, alpha]  # gray
        #         ax.voxels(w, facecolors=colors)

def extract_walls(space, dims, wall_marker):
        lower = [d * 0 for d in dims]
        ranges = [ range(l, d+1) for l,d in zip(lower, dims) ]
        walls = []
        points = product(*ranges)
        for p in points:
                # print(p, end=" ")
                if value_in_euclidean_n_space(space, p) == wall_marker:
                        walls.append(list(p))

        return walls

        



def test():
        from collections import namedtuple
        point4D = namedtuple("point4D", ["x", "y", "z", "w"])
        sol = [ point4D(1,1,1,1), point4D(1,1,1,0), point4D(1,1,0,0), point4D(0,1,0,0), point4D(0,0,0,0) ]

        z = zip(*sol)
        z = tuple(z)
        print(z)

