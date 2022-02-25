try:
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import numpy as np
except Exception as e:
        print(e)

from typing import List

def plot_space(path:List, start, target, title): 
        
        dimensions = tuple(zip(*path))
        # x = [0,0,1,1,2,2]
        # y = [0,1,1,2,2,3]
        # z = [0,0,1,1,2,2]

        fig = plt.figure(figsize=(4,4))

        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(title)


        # ax.scatter(2,3,4) # plot the point (2,3,4) on the figure
        # ax.plot(x,y,z)
        ax.scatter(*start)
        ax.scatter(*target)
        
        ax.plot(*dimensions)

        plt.show()


def test():
        from collections import namedtuple
        point4D = namedtuple("point4D", ["x", "y", "z", "w"])
        sol = [ point4D(1,1,1,1), point4D(1,1,1,0), point4D(1,1,0,0), point4D(0,1,0,0), point4D(0,0,0,0) ]

        z = zip(*sol)
        z = tuple(z)
        print(z)

