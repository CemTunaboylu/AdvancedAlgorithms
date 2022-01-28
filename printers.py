
def n_d_printer(tensor, compare_func, path, color='\033[35m'):

    for x in tensor:
        if isinstance(x, list):
            # print color + str(elm) + '\033[0m', 
            n_d_printer(x, compare_func, color)
        else:

            m = (color + "o" + '\033[0m' ) if x else "X"
            print(m, end=" ")
    print()

# print '\033[35m' + str(elm) + '\033[0m', 
