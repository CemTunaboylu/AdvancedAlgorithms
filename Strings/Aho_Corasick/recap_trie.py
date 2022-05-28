
from typing import Hashable, Iterable, Union, List
 
class TrieNode:
    def __init__(self):
        self.children = dict()
        self.terminal = False
    def __contains__(self, key)->str: 
        return key in self.children
    def __delitem__(self, key):
        if key in self.children:
            del self.children[key]
        else:
            raise KeyError(f"Key '{key}' is not in the children")
    def __getitem__(self, key:Hashable)->Union[None, 'TrieNode']: 
        if key in self.children: return self.children[key]
        else: return None 

    def __iter__(self):
        for ch in self.children:
            yield ch
    def __len__(self)->int: return len(self.children)
    def __repr__(self)->str: return self.__str__()
    def __setitem__(self, key, value):
        if not key in self.children:
            self.children[key] = value 
    def __str__(self)->str: pass

    @classmethod
    def create_trie_node(cls):
        return cls()

def add_seq(trie:TrieNode, seq:Iterable)->bool:
    if trie == None: return False
    
    marcher = trie
    for s in seq:
        if s in marcher:
            marcher = marcher[s]
        else:
            marcher[s] = TrieNode.create_trie_node()
            marcher = marcher[s]

    if marcher.terminal: return False # it was there already, we did not do anything
    
    marcher.terminal = True
    return marcher.terminal

def find_seq(trie:TrieNode, seq:Iterable)->bool:
    if trie == None: return False
    marcher = trie
    for s in seq:
        if not s in marcher: return False
        else:
            marcher = marcher[s]
        
    return marcher.terminal

def del_seq(trie:TrieNode, seq:Iterable)->bool:
    if trie == None: return False

    deleted = [False]
    trie = _del(trie, seq, deleted)

    return deleted[0]

def _del(trie:TrieNode, seq:Iterable, is_deleted:List[bool])->bool:
    if trie == None: return None
    if not seq:
        if trie.terminal: 
            trie.terminal = False
            is_deleted[0] = True
        if trie: # if no children, we are at a leaf
            del trie
            trie = None
        return trie

    next = seq[0]
    if next in trie:
        trie[next] = _del(trie[next], seq[1:], is_deleted )
        if not trie.terminal and trie and is_deleted[0]: # not terminal & trie has no children & deletion is succesful at the leaf
            del trie
            trie = None

    return trie

def print_trie(trie:TrieNode, so_far:List=[]):
    if trie == None: return
    if trie.terminal: print(so_far) 

    for child in trie:
        if child != None:
            print_trie(trie[child], so_far + [child] )
            


def test_add(trie:TrieNode, words:List):
    for w in words:
        r = add_seq(trie, w)
        print(f"'{w}' is {'added' if r else 'cannot be added'} ")
    print_trie(trie)

def test_find(trie:TrieNode, words:List):
    for w in words:
        r = find_seq(trie, w)
        print(f"'{w}' {'is found' if r else 'cannot be found'} ")
        r = find_seq(trie, w[1:])
        print(f"'{w[1:]}' {'is found' if r else 'cannot be found'} ")
    print_trie(trie)

def test_del(trie:TrieNode, words:List):
    for w in words:
        r = del_seq(trie, w)
        print(f"'{w}'  {'is deleted' if r else 'cannot be deleted'} ")
        r = del_seq(trie, w[1:])
        print(f"'{w[1:]}' {'is deleted' if r else 'cannot be deleted'} ")
    print_trie(trie)


if __name__ == "__main__":
    trie = TrieNode.create_trie_node()
    words = ['hack', 'hac', 'hak' ]
    test_add(trie, words)
    test_find(trie, words)
    test_del(trie, words)
