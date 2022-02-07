from operator import __lt__, __gt__

class Heap:
        def __init__(self, arr=[None], min=True):
                self.compare_method = __lt__ if min else __gt__
                self.arr = arr
                self.heapify()
        def level_order(self): 
                lv = 0
                pos = 0
                while pos < len(self.arr):
                        amt = pow(2, lv)
                        print( self.arr[pos:pos+amt] )
                        pos += amt
                        lv += 1

        def percolate_down(self, index):
                cur = index
                left = self.get_left_child(index)
                right = self.get_right_child(index)

                if left < len(self.arr) and self.compare_method( self.arr[left], self.arr[cur] ): cur = left 
                if right < len(self.arr) and self.compare_method( self.arr[right], self.arr[cur] ): cur = right

                if cur != index:
                        self.arr[index], self.arr[cur] = self.arr[cur], self.arr[index] 
                        self.percolate_down(cur)
        
        def percolate_up(self, index, c):
                if not index: return 
                p = self.get_parent(index)
                cur = index
                if self.compare_method(self.arr[index], self.arr[p]):  cur = p
                if index != cur:
                        self.arr[cur], self.arr[index] = self.arr[index], self.arr[cur]
                        c[0] = cur
                        self.percolate_up(cur,c)

        def heapify(self):
                for i in range(len(self.arr)//2-1, -1, -1): # building a heap becomes O(n) with this 
                        self.percolate_down(i)

        def get_left_child(self, index):
                return 2*index+1
        def get_right_child(self, index):
                return 2*index+2
        def get_parent(self, index):
                if index == 0:
                        return None
                return index // 2
        def push(self, elm):
                self.arr.append(elm)
                l = len(self.arr)-1
                r = [l]
                self.percolate_up(l, r)
                return r[0] 
        def pop(self):
                popped = self.arr[0]
                self.arr[0] = self.arr[-1]
                del self.arr[-1]
                self.percolate_down(0)
                return popped

def test_min():
        l = list(range(10,0,-1))
        h = Heap(l)
        from random import randint, choice, seed
        seed(9)
        R = 5
        indices = [None]*R
        for _ in range(R):
                n = randint(0,15)
                i = h.push( n )
                indices[_] = (i, n)
        print(h.arr)
        print(indices)
        for _ in range(R):
                p = h.pop()
                print(f"Popped : {p}")
        print(h.arr)

