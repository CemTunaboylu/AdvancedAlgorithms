matrix = []
stop = False
thread_paths = []

def color_solution_path(m, path, color='\033[35m'):
    if path == None:
        return
    print "------------------------------------------------------------------------------------------------"
    for y,row in enumerate(m):
        print "[ ",
        for x,elm in enumerate(row):
            if any( x == p.x and y == p.y for p in path):
                print color + str(elm) + '\033[0m', 
            else:
                print str(elm),

        print(" ]")
    print "------------------------------------------------------------------------------------------------"

def color_points( points, cur ):
    global matrix
    print "------------------------------------------------------------------------------------------------"
    for y,row in enumerate(matrix):
        print "[ ",
        for x,elm in enumerate(row):
            if any(elm.is_same(p) for p in points):
                print '\033[35m' + str(elm) + '\033[0m', 
            elif cur.x == x and cur.y == y:
                print '\033[92m' + str(elm) + '\033[0m', 
            elif elm.visited :
                print '\033[93m' + str(elm) + '\033[0m', 
            else:
                print str(elm),

        print(" ]")
    print "------------------------------------------------------------------------------------------------"