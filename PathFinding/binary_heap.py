from typing import List, Callable
from operator import __lt__, __gt__


class DuplicateElementException(Exception):pass
class EmptyHeapException(Exception):pass


def assign_key(elm, new_prio):
    return new_prio

class BinaryHeap:
    def __init__(self, elms:List=[], comp_method:Callable= __lt__, assign_key:Callable=assign_key):
        self.heap = elms
        self.element_positions = dict()
        self.prepare_elm_positions()
        self.compare = comp_method
        self.assign_key_method = assign_key

    def __len__(self):
        return len(self.heap)

    def decrease_key(self, elm, new_key):
        if not elm in self.element_positions: raise KeyError(f"{elm} not in elements.")

        index = self.element_positions[elm]
        new_elm = self.assign_key_method(index, new_key)
        self.heap[index] = new_elm
        del self.element_positions[elm]
        self.element_positions[new_elm] = index
        self.percolate_up(index)

    def get_left_child(self, index:int)->int:
        return 2*index+1

    def get_right_child(self, index:int)->int:
        return 2*index+2

    def get_parent(self, index:int)->int:
        if index <= 0: return None
        return index//2

    def heapify(self): 
        for i in range(len(self.heap)//2-1,-1, -1): self.percolate_down(i)

    def level_order(self):
        """ 1, 2, 4, ... """
        begin = 0
        num_elm = 0
        while True:
            pow_2 = 2**begin
            begin += 1
            if num_elm >= len(self.heap): return
            print(f" {self.heap[num_elm: num_elm+pow_2]} ")
            num_elm += pow_2 

    def percolate_down(self, index:int):
        assert index < len(self.heap)

        cur = index 
        left = self.get_left_child(index)
        right = self.get_right_child(index)

        # compare returns True if the first < second
        if left < len(self.heap) and self.compare(self.heap[left], self.heap[cur]): cur = left
        if right < len(self.heap) and self.compare( self.heap[right], self.heap[cur]): cur = right

        if cur != index:
            self.heap[index], self.heap[cur] = self.heap[cur], self.heap[index]
            # the indexes of the heap elements so that we can retrieve them in decrease_key at O(1)
            self.element_positions[self.heap[index]] , self.element_positions[self.heap[cur]] = self.element_positions[self.heap[cur]], self.element_positions[self.heap[index]] 
            self.percolate_down(cur)

    def percolate_up(self, index:int):
        if index == None: return 
        p = self.get_parent(index)
        cur = index

        if p != None and self.compare( self.heap[cur], self.heap[p] ) : cur = p

        if cur != index:
            self.heap[cur], self.heap[index], = self.heap[index], self.heap[cur]
            self.element_positions[self.heap[index]] , self.element_positions[self.heap[cur]] = self.element_positions[self.heap[cur]], self.element_positions[self.heap[index]] 

            self.percolate_up(p)

    def prepare_elm_positions(self):
        for i,e in enumerate(self.heap):
            if not e in self.element_positions:
                self.element_positions[e] = i
            else: raise DuplicateElementException(f"Element {e} is already in the element_positions dictionary")

    def pop(self):
        if not self.heap: raise EmptyHeapException()
        elm = self.heap[0]
        del self.element_positions[elm]

        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        if self.heap:
            self.element_positions[self.heap[0]] = 0
            self.percolate_down(0)

        return elm


    def push(self, elm):
        if elm in self.element_positions: raise DuplicateElementException(f"{elm} is already in the heap")

        new_pos = len(self.heap)
        self.element_positions[elm] = new_pos
        self.heap.append(elm)

        self.percolate_up(new_pos)
                


def heapify_test():
    import heapq
    from random import randint, seed

    seed(9)
    LENGTH, RANGE = 100, 100
    l = [ randint(-RANGE, RANGE) for i in range(LENGTH) ]
    l = list(set(l))
    bheap = BinaryHeap(l[:])
    bheap.heapify()

    heapq.heapify(l)

    # print(f"l : {l}")
    # print(f"bheap : {bheap.heap}")
    # print(f"heapq : {l}")
    assert l == bheap.heap

    print(f"elm pos : {bheap.element_positions}")

def up_test():
    LENGTH = 100
    l = [ i for i in range(1, LENGTH) ]
    bheap = BinaryHeap(l[:])

    bheap.heap.append(0)
    bheap.element_positions[0] = LENGTH-1
    
    bheap.percolate_up(LENGTH-1)

    print(f"bheap : {bheap.heap}")
    print(f"elm pos : {bheap.element_positions}")

def decrease_test():
    LENGTH = 100
    l = [ i for i in range(0, LENGTH) ]
    bheap = BinaryHeap(l[:])

    bheap.decrease_key(LENGTH-1, -1)

    print(f"bheap : {bheap.heap}")
    print(f"elm pos : {bheap.element_positions}")

def pop_test():
    LENGTH = 100
    l = [ i for i in range(0, LENGTH) ]
    l.reverse()
    bheap = BinaryHeap(l[:])
    bheap.heapify()

    min =  bheap.pop()
    print(f"min : {min}")
    print(f"bheap : {bheap.heap}")
    print(f"elm pos : {bheap.element_positions}")
    assert not 0 in bheap.element_positions

def push_test():
    LENGTH = 100
    l = [ i for i in range(0, LENGTH) ]
    l.reverse()
    bheap = BinaryHeap(l[:])
    bheap.heapify()

    new_elm = -100
    min =  bheap.push(new_elm)
    print(f"bheap : {bheap.heap}")
    print(f"elm @ pos : {bheap.element_positions[new_elm]}")


def level_test():
    LENGTH = 100
    l = [ i for i in range(0, LENGTH) ]
    l.reverse()
    bheap = BinaryHeap(l[:])
    bheap.heapify()

    print(f"LV ORDER : ")
    bheap.level_order()


def len_test():

    LENGTH = 10
    l = [ i for i in range(0, LENGTH) ]
    l.reverse()
    bheap = BinaryHeap(l[:])
    bheap.heapify()

    while bheap:
        try:
            e = bheap.pop()
            print(f"popped {e}")
        except Exception as e:
            print(e)
# heapify_test()
# up_test()
# decrease_test()
# pop_test()
# push_test()
# level_test()
len_test()
