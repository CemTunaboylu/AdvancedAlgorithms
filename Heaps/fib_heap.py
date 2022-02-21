from ast import Call
from curses import keyname
from email.generator import Generator
from typing import Callable, Hashable, Iterable, Any
from collections import defaultdict

# Damon Wischik : https://gitlab.developers.cam.ac.uk/djw1005/algorithms/-/blob/master/fibheap.py
# Changed the following
# Change the heap such that IndexErrors are handled vie defaultdict and made silent, push -> alraedy in then decrease_key, vice-versa


def not_found_in_heap(*args, **kwargs):
        return None


class FibHeap:
        class Node:
                def __init__(self, _id, _k ) -> None:            
                        self.child = None
                        self.degree = 0
                        self.ID = _id
                        self.key = _k
                        self.is_loser = False 
                        self.next_sibling = None
                        self.parent = None
                        self.prev_sibling = None


        def __init__(self, xs: Iterable[Hashable]=None,*, sort_key: Callable[[Hashable], float]  )->None:
                self.key_func = sort_key
                self.min_root = None
                self.nodes = defaultdict(not_found_in_heap, {})
                self.root_list = []
                self.values = set()
                if xs is not None:
                        for x in xs:
                                self.push(x)
                        

        def push(self, x:Hashable)->None:
                if x in self.values: # we have such a node, thus we should be decreasing its key if smaller than the one within the heap, or stop 
                        # raise IndexError(f"{x} is already in the heap")
                        if self.nodes[x].key > self.key_func(x):
                                self.decrease_key(x)
                        return
                self.values.add(x)
                n = FibHeap.Node(_id=x, _k=self.key_func(x))
                self.nodes[x] = n
                self._push(n)

        def decrease_key(self, x:Hashable)->None:
                n = self.nodes[x] # no more IndexError
                if not n: 
                        self.push(x)
                        return 
                n.key = self.key_func(x)
                self._decreased_key(n)

        def pop_min(self)->Hashable:
                n = self._pop_min()
                x = n.ID
                del self.nodes[x]
                self.values.remove(x)
                return x

        def __bool__(self) -> bool:
                return (self.min_root is not None)
        def is_empty(self) -> bool:
                return not self.__bool__()

        def __contains__(self, x:Hashable) -> bool:
                return (x in self.values)

        # arrange siblings and update min_root
        def _push(self, n: 'FibHeap.Node'):
                if self.min_root == None:
                        (n.next_sibling, n.prev_sibling) = (n,n)
                        self.min_root = n
                else:
                        self._add_sibling(self.min_root, n, n)
                        if n.key < self.min_root.key:
                                self.min_root=n 

        def _decreased_key(self, n:'FibHeap.Node'):
                if n.parent is None:
                        if n.key < self.min_root.key:
                                self.min_root = n
                elif n.key >= n.parent.key:
                        pass
                else: # Now, dump all the nodes that has to be dumped into the rootlist, and update the tree
                        while n.parent is not None:
                                self._make_orphan(n)
                                u = n.parent
                                (n.parent, n.is_loser) = (None, False)
                                self._add_sibling(self.min_root, n, n)
                                if self.min_root.key > n.key:
                                        self.min_root = n
                                if u.parent is None: # n's parent is a root
                                        break
                                if not u.is_loser:
                                        u.is_loser = True
                                        break
                                n = u
        def _pop_min(self)->'FibHeap.Node':
                if self.min_root is None:
                        return None # silent 
                res = self.min_root
                u,v = (res.prev_sibling, res.next_sibling)
                # u - min_root - v
                if v is res and res.child is None: # only node in tree
                        self.min_root = None
                        return res
                if res.child is not None:
                        for t in FibHeap._siblings(res.child):
                                (t.parent, t.is_loser) = (None, False)
                if u is res: # the only tree in the heap
                        self.min_root = res.child
                else:
                        (u.next_sibling, v.prev_sibling) = (v,u)
                        if res.child is not None:
                                self._add_sibling(u, res.child, res.child.prev_sibling)
                        self.min_root = u
                self.clean_up()
                return res

        def clean_up(self):
                root_array = {}
                for t in FibHeap._siblings(self.min_root):
                        (t.prev_sibling, t.next_sibling) = (t,t)
                        x = t
                        while x.degree in root_array:
                                u = root_array[x.degree]
                                del root_array[x.degree]
                                x = FibHeap._merge(x,u)
                        root_array[x.degree] = x
                u,v = None,None
                for w in root_array.values():
                        if u is None:
                                u,v = w,w
                        else:
                                (v.next_sibling, w.prev_sibling) = (w, v)
                                v = w
                        if w.key < self.min_root.key:
                                self.min_root = w
                (u.prev_sibling, v.next_sibling) = (v,u)
                                
        @staticmethod
        def _add_sibling(n : 'FibHeap.Node', c : 'FibHeap.Node', d : 'FibHeap.Node'):
                """ n-m , c-d -> n-c-d-m """
                m = n.next_sibling
                (n.next_sibling, c.prev_sibling) = (c,n)
                (d.next_sibling, m.prev_sibling) = (m,d)


        @staticmethod
        def _make_orphan(x : 'FibHeap.Node'):
                (u,v) = x.prev_sibling, x.next_sibling
                if v == x: # only child
                        x.parent.child = None
                        x.parent.degree = 0
                else:
                        if x.parent.child == x:
                                x.parent.child = v
                        x.parent.degree -= 1
                        (u.next_sibling, v.prev_sibling) = (v,u)

        @staticmethod
        def _merge(t1 : 'FibHeap.Node', t2 : 'FibHeap.Node') -> 'FibHeap.Node':
                if t1.key > t2.key: (t1,t2) = (t2,t1)
                t1.degree += 1
                t2.parent = t1
                if t1.child is None:
                        t1.child = t2
                else:
                        FibHeap._add_sibling(t1.child, t2, t2)
                return t1

        @staticmethod
        def _siblings(x : 'FibHeap.Node')-> Generator: #-> Generator['FibHeap.Node', None, None]
                #next_u guarantees that when user messes with yielded u, we still have the next sibling no matter what
                start, u, next_u = (x, x, x.next_sibling) 
                yield u 
                while next_u != start:
                        u, next_u = (next_u, next_u.next_sibling)
                        yield u 
        
        def __str__(self) -> str:
                if self.min_root is None:
                         return "Empty heap"
                res = '\n'.join(self._nodestr(c) for c in FibHeap._siblings(self.min_root))
                res = ['.'] + ['|'+r for r in res.splitlines()] + ["'"]
                return '\n'.join(res)
        def _nodestr(self, n: 'FibHeap.Node') -> str:
                self_str = f'{n.ID}({n.key})'
                if n.is_loser: self_str = '{'+self_str+'}'
                if n.child is None:
                        return self_str
                res = []
                cs = [self._nodestr(c) for c in FibHeap._siblings(n.child)]
                imax = len(cs) - 1
                for i,c in enumerate(cs):
                        ls = c.splitlines()
                        jmax = len(ls) - 1
                        for j,l in enumerate(ls):
                                if j>0 and i==imax:
                                        pipe = ' '
                                elif j>0:
                                        pipe = '|'
                                elif imax==0:
                                        pipe = '-'
                                elif i<imax:
                                        pipe = '+'
                                else:
                                        pipe = '\\'
                                r = self_str if i==0 and j==0 else ' '*len(self_str)
                                res.append(r + pipe + l)
                return '\n'.join(res)