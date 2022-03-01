"""
The complexity of the algorithm is linear in the length of the strings plus the length of the searched text plus the number of output matches. 
Note that because all matches are found, there can be a quadratic number of matches if every substring matches (e.g. dictionary = a, aa, aaa, aaaa and input string is aaaa).
These extra internal links allow fast transitions between failed string matches (e.g. a search for cat in a trie that does not contain cat, but contains cart, and thus would fail at the node prefixed by ca), 
to other branches of the trie that share a common prefix (e.g., in the previous case, a branch for attribute might be the best lateral transition). 
This allows the automaton to transition between string matches without the need for backtracking.
When the string dictionary is known in advance (e.g. a computer virus database), the construction of the automaton can be performed once off-line and the compiled automaton stored for later use. 
In this case, its run time is linear in the length of the input plus the number of matched entries.
"""

from collections import defaultdict, deque
from trie import TrieNode
from typing import Hashable, Iterable, List
from sys import path
path.append("..")
from pretty_ux import CHAINS as PREFIX_FOR_KEYWORD_PRINTING
"""
 Have a dict for faillinks and dictionary links, in form of : { <symbol> : <TrieNode>  }
 Have an array of Nodes ? ID is the index, arr[<id>] : Node where Node.id == <id>

class ACNode additionally will have : 
    parent ? # back_track to find the string at that moment? Or we can compute it and give it in the dictionary or have another one for this purpose

"""


# First form the Trie, each time a child is formed, give the current one as its parent in the recursive call
# Then, do BFS, states of d=1 - a.k.a. direct children of the initial state, their fail links are to state 0.
# For each state of depth d, operate on d-1 to find the links
# dict links : follow failure links until you hit the initial state or a terminal node 
# After it is done, let us increment the trie to be faster

ID = 0

class ACNode(TrieNode):
    def __init__(self, _parent = None):
        super().__init__()
        self.parent = _parent
        self.fail_link = None
        self.dict_link = None # if there is, a terminal state (an accepted sequence) which is reached from following failure links along.  
        global ID 
        self.id = ID 
        ID += 1

    # Let us make the class iterable and indexable
    def __contains__(self, symbol)->bool:
        if not symbol in self.children:
            # del self.children[symbol] # defaultdict produces symbol : None, it will mess with our __len__ function
            return False
        return True
    def __getitem__(self, index:Hashable)->TrieNode:
        if index not in self.children:
            return None
        else: return self.children[index] # self.children is a dict

    def __setitem__(self, key, value):
        self.children[key] = value

    def __delitem__(self, key):
        del self.children[key]
    def __iter__(self):
        # if len(self) == 0: raise StopIteration
        keys = self.children.keys()
        for k in keys:
            yield k, self.children[k] # key, value
    def __len__(self): # substitutes has_children() method
        return len(self.children.keys())

    def __str__(self):
        return f" s:{self.id} , states : ({tuple(self.children.keys())}) " #  parent : '{self.parent}'

    def __repr__(self): return str(self)
    
    @classmethod
    def create_node(cls, parent=None):
        return cls(parent)

def put_children_in_queue_with_symbols(node:ACNode, queue:deque):
    for char, children in node:
        queue.append( (char, children) )



class ACAutomaton:
    def __init__(self, init_state=None):
        if init_state == None:
            init_state  = ACNode.create_node()
        self.initial_state = init_state

    def form_faillinks(self): 
        # set all the d=1 states' faillinks into the initial node
        marcher = self.initial_state
        children = []
        for _, child in marcher:
            child.fail_link = marcher
            children.append(child)
        from collections import deque
        queue = deque()
        for ch in children:
            put_children_in_queue_with_symbols(ch, queue)
        while len(queue) > 0:
            # take the symbol and state
            suffix = deque()
            symbol, state = queue.popleft()
            suffix.append(symbol)
            faillink = state.parent.fail_link
            while suffix[-1] not in faillink and faillink.parent != None: # go_to(faillink, symbol) = fail OR faillink = initial state
                faillink = faillink.parent.fail_link
                # if go_to fails, we go up by 1, thus we extend the suffix. We need a stack to take care of that 
                suffix.append(symbol)
            # we have reached a state where go_to(faillink, symbol) != fail
            if faillink == self.initial_state: # could not find
                state.fail_link = faillink[suffix[0]] if suffix[0] in faillink else faillink
            else: state.fail_link = faillink
            suffix.clear()
            put_children_in_queue_with_symbols(state, queue)




    def form_dictlinks(self): pass 

    def add_seq(self, sequence)->bool: 
        if self.initial_state == None : self.initial_state = ACNode.create_node()

        marcher = self.initial_state
        for symbol in sequence:
            if symbol not in marcher:
                marcher[symbol] = ACNode.create_node(marcher) 
            marcher = marcher[symbol]

        if marcher.terminal: return False # already here

        marcher.terminal = True
        return marcher.terminal

    def del_seq(self, sequence)->bool: 
        if not sequence: return False
        if self.initial_state == None: return False
        
        is_done = [False]
        self.initial_state = ACAutomaton._del_internal(self.initial_state, sequence, is_done)

        return is_done[0]
    @staticmethod
    def _del_internal(node:ACNode, sequence:Iterable, is_done:List)->ACNode:
        if node == None: return node
        if not sequence: # consumed the sequence 
            if node.terminal:
                node.terminal = False # the info indicating that the string is in is now eradicated
                is_done[0]=True

            if len(node) == 0: # no children, no point to store this then
                del node
                node = None
            return node

        # recurse through the trie until we get the final symbol
        next = sequence[0] 
        node[next] = ACAutomaton._del_internal(node[next], sequence[1:], is_done)
        if node[next] == None: del node[next] # defaultdict will have next : None thus len(node) will be > 0

        if is_done[0] and len(node) == 0 and not node.terminal:
            del node
            node = None
        return node 

    def find_seq(self, sequence:Iterable)->bool: 
        marcher = self.initial_state
        for symbol in sequence:
            if symbol not in marcher: return False
            marcher = marcher[symbol]

        return marcher.terminal # if it is not terminal, it is not in. 

    @staticmethod
    def print_automaton(n:ACNode, str_so_far:str=""):
        if n.terminal:
            print(f"{PREFIX_FOR_KEYWORD_PRINTING}  {str_so_far} w/ id : {n.id}")

        for char, child in n:
            ACAutomaton.print_automaton(child, str_so_far + char)

    def __len__(self): return len(self.initial_state)

        
