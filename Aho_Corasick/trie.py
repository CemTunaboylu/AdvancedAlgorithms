from collections import defaultdict
from typing import Iterable, List, Tuple
def no_key(*args, **kwargs): return None

"""
Can we implement TrieNode sich that TrieNode[x] gives the TrieNode.children[x]??
"""
class TrieNode:
        def __init__(self):
                self.children = defaultdict(no_key)
                self.terminal = False

        def __str__(self): return f" {'|' if self.terminal else ''} => {self.children} "
        def __repr__(self): return self.__str__()

def create_node():
        return TrieNode()

def add(node:TrieNode, sequence:Iterable)->bool:
        if not node: return False
        marcher = node
        for s in sequence:
                if marcher.children[s] == None:
                        marcher.children[s] = create_node()
                marcher = marcher.children[s]

        if marcher.terminal: return False
        marcher.terminal = True
        return marcher.terminal


def find(node:TrieNode, sequence:Iterable)->bool:
        if not node: return False
        marcher = node
        for s in sequence:
                if marcher.children[s] == None: 
                        del marcher.children[s] # defualtdict creates s : None key value pair when we check
                        return False
                marcher = marcher.children[s]

        return marcher.terminal

def delete(node:TrieNode, sequence:Iterable)->Tuple[bool, TrieNode]:
        result = [False]
        if not node: return (result[0], node) # there is nothing to delete 

        n =  _delete(node, sequence, result)
        return result[0], n 

def has_children(node:TrieNode)->bool:
        if not node: return False
        return len(node.children.keys()) > 0

def _delete(node:TrieNode, sequence:Iterable, success:List[bool])->TrieNode:
        if not node : return node
        if not sequence: # reached the end
                if node.terminal: 
                        node.terminal = False
                        success[0] = True
                if not has_children(node):
                        del node
                        node = None
                return node

        next = sequence[0]
        node.children[next] = _delete(node.children[next], sequence[1:], success)
        if node.children[next] == None: del node.children[next] # defauldict will create next : None, let's clean it
        if success[0] and not has_children(node) and not node.terminal:
                del node
                node = None

        return node 

def print_trie(node:TrieNode):
        if not node: print(f"Trie is empty.")

        _print_trie(node)
def _print_trie(node:TrieNode, so_far:List=[]):
        if node.terminal:
                print(f"word : {''.join(so_far)}") 

        for child,node in node.children.items():
                if child:
                        _print_trie(node, so_far + [child])

